// This file may be redistributed and modified only under the terms of
// the GNU Lesser General Public License (See COPYING for details).
// Copyright 2000 Stefanus Du Toit.
// Automatically generated using gen_cc.py.

#include "Logout.h"

using namespace std;
using namespace Atlas;
using namespace Atlas::Message;

namespace Atlas { namespace Objects { namespace Operation { 

Logout::Logout()
     : Login()
{
    SetAttr("id", string("logout"));
    Object::ListType parents;
    parents.push_back(string("login"));
    SetAttr("parents", parents);
}

Logout Logout::Instantiate()
{
    Logout value;

    Object::ListType parents;
    parents.push_back(string("logout"));
    value.SetAttr("parents", parents);
    value.SetAttr("objtype", string("op"));
    
    return value;
}

} } } // namespace Atlas::Objects::Operation
