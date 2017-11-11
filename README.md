# Waldo Photos Engineering Project

The goal of this project is to produce a working system that can be used as a conversation piece during your on-site interview. Be prepared to:

* Present your solution to a group of smart engineers like yourself.
* Talk about the decisions that went into the creation of your solution.
* Explain how you see the solution evolving over time.
* Discuss the runtime characteristics of the system.
* Discuss technical design tradeoffs and the cost-benefit analysis of those decisions.

### Deliverable

Using any language and data-store of your choice, write a console application that takes two arguments. The arguments are locations of two image files.

Example:
```bash
subimage ./images/image1.jpeg ./images/image2.jpeg
```

The application should return information if one of the images is a cropped part of the other one. If yes, the application should also return the position of top-left
corner of the cropped image within the original image.

Notes:
 - The images may be provided in any order (the cropped image may be the first or the second).
 - The application should work well on JPEGs with some lossy compression enabled.

You can make any additional assumptions, as long as you are explicit about these.

Please deliver the finished project in a publicly available repository on Github. Please title the repository as `waldo-${ github-handle }`.

Deliveries via private repos, BitBucket, or anything other than what is specified above will be disqualified.

### Evaluation

The main areas we will be evaluating are:

- organization of responsibility
- performance
- resilience to failures.

# Analysis

At first glance, this is a computer vision problem.

There are really 2 major pieces to it:

1. Is one picture a subset of the other?
2. Where is the top left pixel?

However, there's a simpler approach: start by looking at the EXIF.

Q: How much can I usefully extract from this by looking at real-world photos?

## Wrinkles

### Manipulated Images

* What about pictures that are rotated?
* Or stretched?
* Or skewed?
* Or color-adjusted?
* Or scaled?

If none of those are possible, then using FFT and cross-correlation would
probably be the way to go.

Answers on StackOverflow recommend using something like SIFT or SURF for
feature detection.

Those depend on a database of existing features.

Realistically, for Waldo Photos, these transformations seem like the most
interesting/relevant:

* Completely different photos of the same location/subjects, at the same time from different angles
* Cropped versions of the same photo (this *is* the key to the homework)
* Color correction

Everything else that I've been pretending might matter is just gravy (at
best).

Although it does need to cope with lossy compression from jpgs.

# Plan of Attack

Deciding whether an image is a subset of another is a fairly straightforward
binary classification problem.

## Training Image Acquisition

We're going to need lots of images for training the network. The more variety
that's involved, the better.

Twitter's firehouse seems like a good starting place. Flickr might be better.

Actually, the imgur API seems like a rich source of random images.

One important detail is that we really don't want the starting set to include
subimages. That's probably best done by hand at first.

## Training Image Manipulation

Once we have a starting library, use something like PIL, scikit-image, or OpenCV
to extract subsets.

For version 1:
Start with the easy version that just clips an image without doing any other
processing.

## Image Analysis

Processing megapixel images seems very likely to be prohibitively expensive.

Of course, scaling them down too much will kill accuracy.

Converting to grayscale seems like it should be safe enough.

Start with the full-blown version and see how well it works.

One of the advantages of using a neural network is that it learns the filtering that
other approaches require.

## Performance Analysis

### Real-time monitoring

It would be great to have a GUI that shows what the various hidden layers are
doing.

It isn't useful for the command-line version we have here, but it's worth keeping
in mind.

### Performance Checking

Need to keep an eye on training curves to be sure results are reasonable.

## This is a couple of dataflow pipelines

I might as well use this as excuse to finish open sourcing my transformers library
and putting it to use. Assuming I *do* write this in python.

Then again, the basic idea of a shell script makes that architecture less attractive.

And, realistically, if this is "just" a neural network, then we don't need as many
pipeline stages as we would otherwise.

Well, treating each layer as a transformation step would be worthwhile if we were
batch processing lots of images.

### Trainer

### Analysis program

## More concretely

Actually, a reasonable starting point might be to start with, say, 50 hand-curated
images. (Q: What are the odds that really will be enough as a useful starting
point?)

Train a neural network with those, then use that to check whether the randomly
acquired images are subsets of each other.

Now pull down more (500 seems like a good starting point) for training.

Slice and dice those, pretty much randomly, to get subsets.

Train against that.

See how well it works and proceed from there.

# That's only the first half!

2nd half is "where is the top left corner?"

Actually, this is a pretty strong indicator that they're probably just looking for an
FFT cross-correlation implementation.

Q: So, do I go with that? Or try to do something innovative?

First alternative approach that comes to mind: binary search.

Start with "is a a subset of b?"

If it is, then split b in half and check again.

That approach seems doomed to fail. This is really a multiclass classification
problem.

Considering the time constraints, this approach will almost definitely require a
prohibitive number of training samples.

Plus my initial thoughts about not needing to preprocess images were
ridiculous. At the very least, they need to start at a uniform size.
