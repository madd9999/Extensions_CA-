# -*- coding: utf-8 -*-
__title__ = "Drop\nImage"
__doc__ = ("Drops an image from the top of the screen to the bottom.\n\n"
           "Put your image in this button folder as drop_image.png "
           "(.jpg/.jpeg/.gif/.bmp also work). Esc or a click closes it.")

import os
import clr

clr.AddReference("PresentationCore")
clr.AddReference("PresentationFramework")
clr.AddReference("WindowsBase")
clr.AddReference("System.Windows.Forms")

from System import TimeSpan
from System.IO import File, MemoryStream
from System.Windows import (Window, WindowStyle, ResizeMode, Point,
                            WindowStartupLocation, Duration, PresentationSource)
from System.Windows.Controls import Canvas, Image
from System.Windows.Input import Key
from System.Windows.Interop import WindowInteropHelper
from System.Windows.Media import Brushes
from System.Windows.Media.Animation import DoubleAnimation, BounceEase, EasingMode
from System.Windows.Media.Imaging import BitmapImage, BitmapCacheOption
from System.Windows.Threading import DispatcherTimer
from System.Windows.Forms import Screen

from pyrevit import forms

# ---------------------------------------------------------------- settings
IMAGE_NAME = "drop_image"   # file name (without extension) to look for
MAX_IMAGE_SIZE = 300        # largest side of the image on screen (DIPs)
FALL_SECONDS = 3          # duration of the fall, bounces included
STAY_SECONDS = 3          # time it rests at the bottom before closing
BOUNCES = 5                 # 0 = no bounce
BOUNCINESS = 2              # higher = smaller bounces
IMAGE_EXTS = (".png", ".jpg", ".jpeg", ".gif", ".bmp")
# -------------------------------------------------------------------------

BUTTON_DIR = os.path.dirname(os.path.abspath(__file__))


def find_image():
    """drop_image.<ext> if present, else the first non-icon image."""
    images = [f for f in sorted(os.listdir(BUTTON_DIR))
              if os.path.splitext(f)[1].lower() in IMAGE_EXTS]
    for f in images:
        if os.path.splitext(f)[0].lower() == IMAGE_NAME:
            return os.path.join(BUTTON_DIR, f)
    for f in images:
        if not f.lower().startswith("icon"):
            return os.path.join(BUTTON_DIR, f)
    return None


def load_bitmap(path):
    """Load from bytes: no file lock, no URI trouble with '#' or '%' in paths."""
    bmp = BitmapImage()
    bmp.BeginInit()
    bmp.StreamSource = MemoryStream(File.ReadAllBytes(path))
    bmp.CacheOption = BitmapCacheOption.OnLoad
    bmp.EndInit()
    bmp.Freeze()
    return bmp


class FallingImageWindow(Window):
    """Transparent, borderless overlay covering Revit's monitor."""

    def __init__(self, bitmap):
        self.WindowStyle = getattr(WindowStyle, "None")  # 'None' is a keyword
        self.AllowsTransparency = True
        self.Background = Brushes.Transparent
        self.Topmost = True
        self.ShowInTaskbar = False
        self.ResizeMode = ResizeMode.NoResize
        self.WindowStartupLocation = WindowStartupLocation.Manual
        WindowInteropHelper(self).Owner = __revit__.MainWindowHandle

        # image scaled down to MAX_IMAGE_SIZE, aspect ratio kept
        w, h = bitmap.Width, bitmap.Height
        k = min(1.0, float(MAX_IMAGE_SIZE) / max(w, h, 1))
        self.img_w, self.img_h = w * k, h * k

        self.image = Image()
        self.image.Source = bitmap
        self.image.Width = self.img_w
        self.image.Height = self.img_h

        self.canvas = Canvas()
        self.canvas.Children.Add(self.image)
        Canvas.SetTop(self.image, -self.img_h)   # start just above the screen
        self.Content = self.canvas

        self.timer = None
        self.closed = False

        self.SourceInitialized += self.on_source_initialized
        self.Loaded += self.on_loaded
        self.Closed += self.on_closed
        self.KeyDown += self.on_key
        self.MouseLeftButtonDown += lambda s, e: self.Close()

    def on_source_initialized(self, sender, args):
        """Cover Revit's monitor, converting screen pixels to WPF DIPs."""
        area = Screen.FromHandle(__revit__.MainWindowHandle).WorkingArea
        to_dip = PresentationSource.FromVisual(self).CompositionTarget.TransformFromDevice
        top_left = to_dip.Transform(Point(area.Left, area.Top))
        bottom_right = to_dip.Transform(Point(area.Right, area.Bottom))
        self.Left, self.Top = top_left.X, top_left.Y
        self.Width = bottom_right.X - top_left.X
        self.Height = bottom_right.Y - top_left.Y

    def on_loaded(self, sender, args):
        try:
            self.Activate()   # so Esc works
            Canvas.SetLeft(self.image, (self.ActualWidth - self.img_w) / 2.0)

            anim = DoubleAnimation()
            anim.From = -self.img_h
            anim.To = self.ActualHeight - self.img_h
            anim.Duration = Duration(TimeSpan.FromSeconds(FALL_SECONDS))
            if BOUNCES > 0:
                ease = BounceEase()
                ease.Bounces = BOUNCES
                ease.Bounciness = BOUNCINESS
                ease.EasingMode = EasingMode.EaseOut
                anim.EasingFunction = ease
            anim.Completed += self.on_fall_done
            self.image.BeginAnimation(Canvas.TopProperty, anim)
        except Exception:
            self.Close()   # never leave an invisible overlay up
            raise

    def on_fall_done(self, sender, args):
        if self.closed:
            return
        self.timer = DispatcherTimer()
        self.timer.Interval = TimeSpan.FromSeconds(STAY_SECONDS)
        self.timer.Tick += lambda s, e: self.Close()
        self.timer.Start()

    def on_closed(self, sender, args):
        self.closed = True
        if self.timer:
            self.timer.Stop()

    def on_key(self, sender, args):
        if args.Key == Key.Escape:
            self.Close()


image_path = find_image()
if not image_path:
    forms.alert("No image found.\n\nPut an image named '{}.png' in:\n{}"
                .format(IMAGE_NAME, BUTTON_DIR), title="Drop Image", exitscript=True)

try:
    bitmap = load_bitmap(image_path)
except Exception as ex:
    forms.alert("Could not load image:\n{}\n\n{}".format(image_path, ex),
                title="Drop Image", exitscript=True)

FallingImageWindow(bitmap).ShowDialog()
