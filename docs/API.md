# image\_compare.find\_sub\_image

This is really the most interesting module here.

## extract_match

Parameters:
* correlation: as returned by calculate_match
* threshold: how good must the "match" be?

Returns: The top left corner of the match

That top left corner is really the first max index in the
correlation array, if any of the features match more
closely than threshold.

If there is no match, then this returns None.

The threshold parameter seems like something that's ripe
for playing with.

I don't have a good feel (yet) for good values. In the
[limited] tests I've run, 0.5 seems "good enough." But
actual clipped images get very close to 1.0.

## calculate_match

Parameters: 2 numpy arrays.
* image (which might contain the template)
* template (aka subimage).

Returns: A "correlation" array that
describes the similarities between the image and the template.

The values in that range from -1 to 1.

## load_images

Parameters:
* name1: Name of one image file to load
* name2: Name of the other image file to load

Returns:
A dict that contains the keys:
* template: smaller image
* image larger image
* template\_name: name of the smaller image file
* image\_name: name of the larger image file

## compare_images

Parameters:
* name1 - name of first image file to consider
* name2 - name of the second image file to consider
* threshold - how much leeway do we provide to matches?

Returns:
A dict that contains the keys:
* template: smaller image
* image larger image
* template\_name: name of the smaller image file
* image\_name: name of the larger image file
* top_left: An (x, y) coordinate pair suitable for plotting.
  Or None, if no match was better than threshold.

In general, just use this. The other functions are really
for fine-grained control during testing.

# image_compare.visualize

This is really a wrapper around find\_sub\_image.compare_images
that adds some graphics to the input to provide some visual
feedback about what's going on.

# image_compare.check

A couple of automated tests just for the sake of sanity.
