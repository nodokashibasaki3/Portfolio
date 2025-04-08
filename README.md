# Personal Portfolio - Nodoka Shibasaki

A personal portfolio website showcasing digital artwork, videos, and blog content with an interactive gallery experience.

## Overview

This portfolio website features:

- **About Page**: Introduction and personal information
- **Blog Section**: Articles and thoughts
- **Interactive Art Gallery**: An immersive gallery experience with seamless looping

## Gallery Features

The interactive gallery provides a unique way to browse through artwork and videos:

- **Seamless Looping**: Continuously scroll through artwork with a seamless transition from end to beginning
- **Responsive Design**: Works on desktop and mobile devices
- **Multiple Navigation Methods**:
  - Mouse/trackpad scrolling
  - Touch controls for mobile devices
  - Keyboard arrow keys
- **Magnifying Glass**: Click on images to activate a magnifying glass effect for detailed viewing
- **Visual Effects**: Hover animations and visual feedback when interacting with artwork

## Technical Details

### Gallery Implementation

The gallery uses a unique approach to create a seamless looping experience:

1. **Duplicate Artwork Set**: The gallery creates two identical sets of artwork
2. **Position Calculation**: Artworks are positioned sequentially with the second set appearing right after the first
3. **Seamless Transition**: When scrolling past the end of the first set, the position resets to the beginning
4. **Responsive Controls**: Different input methods (scroll, touch, keyboard) are supported

### File Structure

- `index.html` - Main about page
- `blog.html` - Blog section
- `gallery.html` - Interactive art gallery
- `style.css` - Main stylesheet
- `assets/` - Directory containing artwork and video files

## Usage

1. Navigate to the gallery page
2. Use your mouse/trackpad to scroll horizontally through the gallery
3. Click on images to activate the magnifying glass effect
4. Use arrow keys as an alternative navigation method
5. On mobile devices, swipe left/right to navigate

## Browser Compatibility

The gallery is designed to work on modern browsers including:
- Chrome
- Firefox
- Safari
- Edge

## Credits

Created by Nodoka Shibasaki 