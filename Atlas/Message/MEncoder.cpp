// This file may be redistributed and modified only under the terms of
// the GNU Lesser General Public License (See COPYING for details).
// Copyright (C) 2000 Stefanus Du Toit

#include "MEncoder.h"
#include "Object.h"

namespace Atlas { namespace Message {

Encoder::Encoder(Atlas::Bridge* b)
    : EncoderBase(b)
{
}

void Encoder::listItem(const Element& obj)
{
    switch (obj.getType()) {
        case Element::TYPE_INT: m_bridge->listItem(obj.asInt()); break;
        case Element::TYPE_FLOAT: m_bridge->listItem(obj.asFloat()); break;
        case Element::TYPE_STRING: m_bridge->listItem(obj.asString()); break;
        case Element::TYPE_MAP: {
            m_bridge->listItem(Atlas::Bridge::m_mapBegin);
            Element::MapType::const_iterator I;
            for (I = obj.asMap().begin(); I != obj.asMap().end();
                    I++)
                mapItem((*I).first, (*I).second);
            m_bridge->mapEnd();
            }
            break;
        case Element::TYPE_LIST: {
            m_bridge->listItem(Atlas::Bridge::m_listBegin);
            Element::ListType::const_iterator I;
            for (I = obj.asList().begin(); I != obj.asList().end();
                    I++)
                listItem(*I);
            m_bridge->listEnd();
            }
            break;
        default: break;
    }
}

void Encoder::mapItem(const std::string& name, const Element& obj)
{
    switch (obj.getType()) {
        case Element::TYPE_INT: m_bridge->mapItem(name, obj.asInt()); break;
        case Element::TYPE_FLOAT: m_bridge->mapItem(name, obj.asFloat()); break;
        case Element::TYPE_STRING: m_bridge->mapItem(name, obj.asString()); break;
        case Element::TYPE_MAP: {
            m_bridge->mapItem(name, Atlas::Bridge::m_mapBegin);
            Element::MapType::const_iterator I;
            for (I = obj.asMap().begin(); I != obj.asMap().end();
                    I++)
                mapItem((*I).first, (*I).second);
            m_bridge->mapEnd();
            }
            break;
        case Element::TYPE_LIST: {
            m_bridge->mapItem(name, Atlas::Bridge::m_listBegin);
            Element::ListType::const_iterator I;
            for (I = obj.asList().begin(); I != obj.asList().end();
                    I++)
                listItem(*I);
            m_bridge->listEnd();
            }
            break;
        default:
            break;
    }                          
}

void Encoder::streamMessage(const Element& obj)
{
    if (obj.isMap()) {
        m_bridge->streamMessage(Atlas::Bridge::m_mapBegin);
        Element::MapType::const_iterator I;
        for (I = obj.asMap().begin();
             I != obj.asMap().end(); I++)
            mapItem((*I).first, (*I).second);
        m_bridge->mapEnd();
    }
}



} } // namespace Atlas::Message
