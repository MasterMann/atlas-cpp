// This file may be redistributed and modified only under the terms of
// the GNU Lesser General Public License (See COPYING for details).
// Copyright 2000 Stefanus Du Toit.
// Automatically generated using gen_cc.py.

#include "Info.h"

using namespace std;
using namespace Atlas;
using namespace Atlas::Message;

namespace Atlas { namespace Objects { namespace Operation { 

Info::Info()
     : RootOperation()
{
    SetAttr("id", string("info"));
    Object::ListType parent;
    parent.push_back(string("root_operation"));
    SetAttr("parent", parent);
}

Info Info::Instantiate()
{
    Info value;

    Object::ListType parent;
    parent.push_back(string("info"));
    value.SetAttr("parent", parent);
    
    return value;
}

} } } // namespace Atlas::Objects::Operation