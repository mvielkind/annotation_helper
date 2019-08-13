# My Annotation Helper Buddy

Recently I've been doing a lot of data annotation.  I've been working on a project to extract a [shopping list from a 
screenshot](https://matthewvielkind.dev/home/2019/6/23/extracting-a-list-from-an-image) that requires a custom NLP model
to be utilized.  Of course to build a custom NLP model requires a fair amount of annotated data, which is a tedious 
task to undertake.  To help with the data annotation I built a lightweight Python class, `AnnotateHelper`, to interact
with in a Jupyter Notebook to help annotate a document.

The class helps to suggest entities that exist in the document, delete, and add tagged entities in the document, complete
with their location in the document.  Taken together `AnnotateHelper` speeds up the time required to annotate identify
the location of named entities in a document.

The attached Jupyter Notebook walks through an example use case of using the class. Feel free to play around and see
if this is something you could find useful!