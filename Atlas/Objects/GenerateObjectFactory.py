#This file is distributed under the terms of 
#the GNU Lesser General Public license (See the file COPYING for details).
#Copyright (C) 2000-2001 Aloril
#Copyright (C) 2001-2005 Alistair Riddoch

#just used to partition gen_cpp.py into files, 
#not usable without GenerateCC class

__revision__ = '$Id$'

from common import *

class GenerateObjectFactory:
    def generate_object_factory(self, objects, max_class_no):
        #print "Output of implementation for:",
        outfile = self.outdir + '/objectFactory.cpp'
        #print outfile
        self.out = open(outfile + ".tmp", "w")
        self.write(copyright_template % ("Aloril", "Alistair Riddoch"))
        self.write('\n#include <Atlas/Objects/objectFactory.h>\n')
        self.write('#include <Atlas/Objects/Entity.h>\n')
        self.write('#include <Atlas/Objects/Anonymous.h>\n')
        self.write('#include <Atlas/Objects/Operation.h>\n\n')
        self.write('#include <Atlas/Objects/Generic.h>\n\n')
        self.ns_open(self.base_list)
        self.write('\nint enumMax = ')
        self.write(str(max_class_no))
        self.write(';\n')
        self.write("""
using Atlas::Message::Element;
using Atlas::Message::ListType;
using Atlas::Message::MapType;

NoSuchFactoryException::~NoSuchFactoryException()
{
}

SmartPtr<RootData> generic_factory(const std::string & name, int no)
{
    Operation::Generic obj;
    obj->setType(name, no);
    return obj;
}

SmartPtr<RootData> anonymous_factory(const std::string & name, int no)
{
    Entity::Anonymous obj;
    obj->setType(name, no);
    return obj;
}

std::map<const std::string, Root> objectDefinitions;

class AddFactories {
public:
    AddFactories();
} addThemHere;

AddFactories::AddFactories()
{
    Factories * objectFactory = Factories::instance();
""") #"for xemacs syntax highlighting
        for (obj, namespace) in objects:
            id = obj.id
            idc = classize(id)
            idu = string.upper(id)
            self.write("""
    objectFactory->addFactory("%(id)s", &factory<%(namespace)s%(idc)sData>, %(namespace)s%(idu)s_NO);
""" % vars()) #"for xemacs syntax highlighting
        self.write("""}

Factories::Factories()
{
}

Factories::Factories(const Factories & other) : m_factories(other.m_factories)
{
}

bool Factories::hasFactory(const std::string& name)
{
    FactoryMap::const_iterator I = m_factories.find(name);
    return I != m_factories.end();
}
    
Root Factories::createObject(const std::string& name)
{
    FactoryMap::const_iterator I = m_factories.find(name);
    if (I == m_factories.end()) {
        return Root(0);
    } else {
        return (*I).second.first(name, (*I).second.second);
    }
}
    
Root Factories::createObject(const MapType & msg_map)
{
    Root obj(0);

    // is this instance of entity or operation?
    MapType::const_iterator I = msg_map.find(Atlas::Objects::OBJTYPE_ATTR);
    MapType::const_iterator Iend = msg_map.end();
    bool is_instance = false;
    if(I != Iend && I->second.isString()) {
        const std::string & objtype = I->second.String();
        if(objtype == "op" || objtype == "obj" || objtype == "object") {
            // get parent
            I = msg_map.find(Atlas::Objects::PARENTS_ATTR);
            if(I != Iend && I->second.isList()) {
                const ListType & parents_lst = I->second.List();
                if(parents_lst.size()>=1 && parents_lst.front().isString()) {
                    const std::string & parent = parents_lst.front().String();
                    // objtype and parent ok, try to create it:
                    FactoryMap::const_iterator I = m_factories.find(parent);
                    if (I != m_factories.end()) {
                        obj = I->second.first(parent, I->second.second);
                    } else {
                        if (objtype == "op") {
                            obj = Atlas::Objects::Operation::Generic();
                        } else {
                            obj = Atlas::Objects::Entity::Anonymous();
                        }
                    }
                    is_instance = true;
                    // FIXME We might want to do something different here.
                } // parent list ok?
            } // has parent attr?
        } // has known objtype
    } // has objtype attr
    if (!is_instance) {
        // Should we really use factory? Why not just instantiate by hand?
        obj = Atlas::Objects::Entity::Anonymous();
    } // not instance
    for (I = msg_map.begin(); I != Iend; I++) {
        obj->setAttr(I->first, I->second);
    }
    return obj;
}

std::list<std::string> Factories::getKeys()
{
    std::list<std::string> keys;
    for (FactoryMap::const_iterator I = m_factories.begin();
         I != m_factories.end(); I++) {
        keys.push_back(I->first);
    }
    return keys;
}
    
void Factories::addFactory(const std::string& name, FactoryMethod method, int classno)
{
    m_factories[name] = std::make_pair(method, classno);
}

int Factories::addFactory(const std::string& name, FactoryMethod method)
{
    int classno = ++enumMax;
    m_factories[name] = std::make_pair(method, classno);
    return classno;
}

Factories * Factories::instance()
{
    if (m_instance == 0) {
        m_instance = new Factories;
    }
    return m_instance;
}

Factories * Factories::m_instance = 0;
""") #"for xemacs syntax highlighting
            
        self.ns_close(self.base_list)
        self.out.close()
        self.update_outfile(outfile)
