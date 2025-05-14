"""
Script for NodeFixturePlacement
"""

import NemAll_Python_BaseElements as AllplanBaseElements
import NemAll_Python_Precast as AllplanPrecast

from NodeUtil import NodeBase, NodeObjectUtil

NodeBase.trace_node_name('NodeFixturePlacement')


def create_node(init_data):
    """
    Create the node

    Args:
        init_data:  data for the node initialization
    """

    return NodeFixturePlacement(init_data)


class NodeFixturePlacement(NodeBase):
    """
    Definition of class NodeFixturePlacement
    """

    def _create_output(self):
        """ Execute the node """

        build_ele = self.build_ele

        self._set_init_node_output(build_ele.FixturePlacement)

        fixture = build_ele.Fixture.value

        if fixture == []:
            self.warning = "Fixture is empty"
            return

        com_prop = AllplanBaseElements.CommonProperties()

        com_prop.GetGlobalProperties()

        fixture_placement_prop = AllplanPrecast.FixturePlacementProperties()

        fixture_placement_prop.Name        = fixture.GetFixtureProperties().Name
        fixture_placement_prop.OutlineType = AllplanPrecast.OutlineType.eBUILTIN_OUTLINE_TYPE_NO_AFFECT
        fixture_placement_prop.ConnectionToAIACatalog = True

        placement = AllplanPrecast.FixturePlacementElement(com_prop, fixture_placement_prop, fixture)


        #----------------- add the attributes

        attr_list = NodeObjectUtil.create_objects_list(build_ele.Attributes.value)

        if build_ele.PlanText.value:
            attr_list.append(AllplanBaseElements.AttributeString(823, build_ele.PlanText.value))

        if attr_list:
            attr_set_list = []
            attr_set_list.append(AllplanBaseElements.AttributeSet(attr_list))

            attributes = AllplanBaseElements.Attributes(attr_set_list)

            placement.SetAttributes(attributes)

        build_ele.FixturePlacement.value = placement
