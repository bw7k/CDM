﻿from typing import List, Optional, TYPE_CHECKING

from cdm.enums import CdmObjectType

from . import extension_helper, utils
from .type_attribute_persistence import TypeAttributePersistence
from .types import LocalEntity

if TYPE_CHECKING:
    from cdm.objectmodel import CdmCorpusContext, CdmEntityDefinition, CdmTraitDefinition, CdmTypeAttributeDefinition
    from cdm.utilities import CopyOptions, ResolveOptions


class EntityPersistence:
    @staticmethod
    async def from_data(ctx: 'CdmCorpusContext', data: 'LocalEntity', extension_trait_def_list: List['CdmTraitDefinition'],
                        local_extension_trait_def_list: List['CdmTraitDefinition']) -> Optional['CdmEntityDefinition']:
        entity = ctx.corpus.make_object(CdmObjectType.ENTITY_DEF, data.name)

        if data.get('description'):
            entity.description = data.description

        await utils.process_annotations_from_data(ctx, data, entity.exhibits_traits)

        for element in (data.get('attributes') or []):
            type_attribute = await TypeAttributePersistence.from_data(ctx, element, extension_trait_def_list, local_extension_trait_def_list)
            if type_attribute is not None:
                entity.attributes.append(type_attribute)
            else:
                ctx.logger.error('There was an error while trying to convert model.json attribute to cdm attribute.')
                return

        extension_helper.process_extension_from_json(ctx, data, entity.exhibits_traits, extension_trait_def_list, local_extension_trait_def_list)

        return entity

    @staticmethod
    async def to_data(instance: 'CdmEntityDefinition', res_opt: 'ResolveOptions', options: 'CopyOptions', ctx: 'CdmCorpusContext') -> Optional['LocalEntity']:
        data = LocalEntity()
        data.type = 'LocalEntity'
        data.name = instance.entity_name
        data.description = instance.description

        await utils.process_annotations_to_data(instance.ctx, data, instance.exhibits_traits)

        if instance.attributes:
            data.attributes = []
            for element in instance.attributes:
                attribute = await TypeAttributePersistence.to_data(element, res_opt, options)
                if attribute:
                    data.attributes.append(attribute)
                else:
                    ctx.logger.error('There was an error while trying to convert cdm attribute to model.json attribute.')
                    return None

        return data
