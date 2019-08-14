# A Lightweight Jupyter Annotation Helper

Recently I've been doing a lot of data annotation.  I've been working on a project to extract a [shopping list from a 
screenshot](https://matthewvielkind.dev/home/2019/6/23/extracting-a-list-from-an-image) that requires a custom NLP model
to be utilized.  Of course to build a custom NLP model requires a fair amount of annotated data, which is a tedious 
task to undertake.  To help with the data annotation I built a lightweight Python class, `AnnotateHelper`, to interact
with in a Jupyter Notebook to help annotate a document.

To get started all you have to do is initialize the `AnnotateHelper` class with the text you want to annotate.

```python
annotate_obj = AnnotateHelper(<text_to_annotate>)
```

One the `AnnotateHelper` class is initialized you can utilize it's methods to help annotate the document.  If you have
an existing NER model you can leverage that model to seed the initial annotations with the `suggest_entities` method.
Utilizing an existing model gives you a place to start with annotating so you don't have to grind through annotating
each entity individually.

Dropping an annotation from a document can be done with the `drop_entity` method by passing the `entity_id` that you
want to drop.

Entities can be added with the `entity_span` method.  Given a phrase `entity_span` will search the document for
occurrences of the phrase and will walkthrough the annotation for each of those occurrences.

Finally, the `save` method saves the class instance for you to incorporate in your NER model.


## A Few Notes.

My use case was focused on shorter length documents the size of a long text message.  I'm not sure how well it would 
work with longer documents, but the format does seem to work well with the shorter documents I'm dealing with.  The 
initial features I've added are pretty sparse.  As I use this utility more I'll expand the functionality.