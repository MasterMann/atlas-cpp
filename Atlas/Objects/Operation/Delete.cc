// This file may be redistributed and modified only under the terms of
// the GNU Lesser General Public License (See COPYING for details).
// Copyright 2000 Stefanus Du Toit.
// Automatically generated using gen_cc.py.

#include "Delete.h"

using Atlas::Message::Object;

namespace Atlas { namespace Objects { namespace Operation { 

Delete::Delete()
     : Action()
{
    SetId(std::string("delete"));
    Object::ListType parents;
    parents.push_back(std::string("action"));
    SetParents(parents);
}

Delete Delete::Instantiate()
{
    Delete value;

    Object::ListType parents;
    parents.push_back(std::string("delete"));
    value.SetParents(parents);
    value.SetObjtype(std::string("op"));
    
    return value;
}

} } } // namespace Atlas::Objects::Operation