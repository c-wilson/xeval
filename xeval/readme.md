# Xeval

## architecture

This was written with the intent of having some ability to expand in the future. There was some thought put 
into the architecture of the program to make it as close to CLEAN as possible.

In its current form, it is a skeleton and some of the modularity seems overkill. I would argue that keeping
separation between these modules will make maintenance and expansion of this system more manageable and
does little to decrease productivity while it is small.

The following design principles were made priorities:

1. Dependencies (ie web framework, database) should be moved outside the main pattern of the program. 
It is perhaps obvious that the database will have to change from the current Python dict implementation to
a relational db.
1. Data models should not depend on views. The web interface may be the current interaction mode, but other
data sources/sinks could become relevant in the future.
1. Algorithms (and business rules) should be kept from depending on data models and views.
1. Use abstract interface classes when possible to allow for migration to a more complex system later. 
For example, you can easily imagine that calculating solutions might be more complex than in this simple example, 
especially when the calculations we're performing are nontrivial. Posting data for a reputee might be 
recorded to the database AND posted to a task queue which will update the reputation score for that reputee 
when computational resources are available.

## structure

### main.py
this is the main entry point for the program and it holds:
 * __Reptor__: main logic handles the logic of the program. 
 * __ReptorResource__: the web framework interface class, interacts with Reptor.
 * JSON schema for POST and GET http transactions.
 * Utility functions for Falcon.
 
 ### algorithms
 this holds the algorithms for calculating reputation. This module is self-contained and just holds the math.
 __This module drives development of other modules.__ It is overkill now, but it is kept separate for
 easier maintenance.

### storage.py
this holds the data structure for the program and an interface to that data structure. This is kept separate
so that it can be easily converted to use a more robust database system in the future.

 * __SimpleStorage__: main entry to the storage module, invokes the data structure.
 * __ReputeeModel__: Data is organized into ReputeeModel objects which contain transactions.
 * __EntryModel__: Each Reputee has many EntryModel instances embedded in it.

### exceptions.py
self explanatory, but this contains Exception classes that are caught by the view framework class methods.