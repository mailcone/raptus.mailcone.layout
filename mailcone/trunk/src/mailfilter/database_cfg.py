#XXX - should be done in a configlet later! 

import grok
from megrok import rdb
from z3c.saconfig import (EngineFactory, GloballyScopedSession)
from z3c.saconfig.interfaces import (IEngineFactory, IScopedSession, IEngineCreatedEvent)

DSN = 'postgresql://user:pw@localhost:5432/mails'

# XXX should be later a local utility
""" XXX - If you want this utility to be persistent, you should subclass it
    and mixin Persistent. You could then manage the parameters
    differently than is done in this __init__, for instance as
    attributes, which is nicer if you are using Persistent (or Zope 3
    schema). In this case you need to override the configuration method.
    """
engine_factory = EngineFactory(DSN, echo=True)
grok.global_utility(engine_factory, provides=IEngineFactory, direct=True)

scoped_session = GloballyScopedSession()
grok.global_utility(scoped_session, provides=IScopedSession, direct=True)

skip_create_metadata = rdb.MetaData()
create_metadata = rdb.MetaData()

@grok.subscribe(IEngineCreatedEvent)
def create_engine_created(event):
    rdb.setupDatabase(create_metadata)

@grok.subscribe(IEngineCreatedEvent)
def skip_create_engine_created(event):
    rdb.setupDatabaseSkipCreate(skip_create_metadata)