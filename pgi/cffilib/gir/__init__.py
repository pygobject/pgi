# Copyright 2013 Christoph Reiter
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.

from .gibaseinfo import GIBaseInfo, GITypelib, GIInfoType
from .girepository import GIRepository, GIRepositoryLoadFlags
from .giarginfo import GIArgInfo, GIDirection, GITransfer, GIScopeType
from .gitypeinfo import GITypeInfo, GIArrayType, GITypeTag
from .giconstantinfo import GIConstantInfo
from .gipropertyinfo import GIPropertyInfo
from .giregisteredtypeinfo import GIRegisteredTypeInfo
from .gifieldinfo import GIFieldInfo, GIFieldInfoFlags
from .gicallableinfo import GICallableInfo
from .gienuminfo import GIEnumInfo, GIValueInfo
from .gifunctioninfo import GIFunctionInfo, GIFunctionInfoFlags, GInvokeError
from .giobjectinfo import GIObjectInfo
from .giunioninfo import GIUnionInfo
from .gistructinfo import GIStructInfo


GIArgInfo = GIArgInfo
GIArrayType = GIArrayType
GIBaseInfo = GIBaseInfo
GICallableInfo = GICallableInfo
GIConstantInfo = GIConstantInfo
GIDirection = GIDirection
GIEnumInfo = GIEnumInfo
GIFieldInfoFlags = GIFieldInfoFlags
GIFieldInfo = GIFieldInfo
GIFunctionInfoFlags = GIFunctionInfoFlags
GIFunctionInfo = GIFunctionInfo
GIInfoType = GIInfoType
GInvokeError = GInvokeError
GIObjectInfo = GIObjectInfo
GIPropertyInfo = GIPropertyInfo
GIRegisteredTypeInfo = GIRegisteredTypeInfo
GIRepository = GIRepository
GIRepositoryLoadFlags = GIRepositoryLoadFlags
GIScopeType = GIScopeType
GIStructInfo = GIStructInfo
GITransfer = GITransfer
GITypeInfo = GITypeInfo
GITypelib = GITypelib
GITypeTag = GITypeTag
GIUnionInfo = GIUnionInfo
GIValueInfo = GIValueInfo
