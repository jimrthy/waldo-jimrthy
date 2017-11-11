# image\_compare.find\_sub\_image

This is really the most interesting module here.

It contains 1 class, Matcher.

## compare_images

Parameters:
* name1 - name of first image file to consider
* name2 - name of the second image file to consider
* threshold - how much leeway do we provide to matches?

Returns: top-left corner of a match, if any

In general, just use this. The other two are really
for fine-grained control during testing.

## calculate_match

Parameters: 2 numpy arrays. 1 for the image (which might
contain the template), 1 for the template (aka subimage).

Returns: None. This function is called for side-effects.

This builds a correlation array (stored in self.correlation) that
describes the similarities between the image and the template.

The values in here range from -1 to 1.

## extract_match

Parameters: threshold

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

# image_compare.visualize

This is really a wrapper around find\_sub\_image.compare_images
that adds some graphics to the input to provide some visual
feedback about what's going on.

# image_compare.check

A couple of automated tests just for the sake of sanity.
