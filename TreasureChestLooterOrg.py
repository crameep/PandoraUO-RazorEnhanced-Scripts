#OrganizeTreasureLootBag
class myItem:
    name = None
    itemID = None
    color = None
    category = None
    weight = None

    def __init__ ( self, name, itemID, color, category, weight ):
        self.name = name
        self.itemID = itemID
        self.color = color
        self.category = category
        self.weight = weight
gems = {
    'amber': myItem(
        name = 'amber',
        itemID = 0x0F25,
        color = 0x0000,
        category = 'gem',
        weight = 0.1
    ),
    'amethyst': myItem(
        name = 'amethyst',
        itemID = 0x0F16,
        color = 0x0000,
        category = 'gem',
        weight = 0.1
    ),
    'citrine': myItem(
        name = 'citrine',
        itemID = 0x0F15,
        color = 0x0000,
        category = 'gem',
        weight = 0.1
    ),
    'diamond': myItem(
        name = 'diamond',
        itemID = 0x0F26,
        color = 0x0000,
        category = 'gem',
        weight = 0.1
    ),
    'emerald': myItem(
        name = 'emerald',
        itemID = 0x0F10,
        color = 0x0000,
        category = 'gem',
        weight = 0.1
    ),
    'rubies': myItem(
        name = 'rubies',
        itemID = 0x0F13,
        color = 0x0000,
        category = 'gem',
        weight = 0.1
    ),
    'sapphire': myItem(
        name = 'sapphire',
        itemID = 0x0F19,
        color = 0x0000,
        category = 'gem',
        weight = 0.1
    ),
    'star sapphire': myItem(
        name = 'star sapphire',
        itemID = 0x0F21,
        color = 0x0000,
        category = 'gem',
        weight = 0.1
    ),
    'tourmaline': myItem(
        name = 'tourmaline',
        itemID = 0x0F2D,
        color = 0x0000,
        category = 'gem',
        weight = 0.1
    )
}
containerID = 0x400732AB

amber = Items.FindByID( gems[ 'amber' ].itemID, 0x0000, containerID )
Items.Move( amber, containerID, 0, 21, 13 )
Misc.Pause( 700 )

amethyst = Items.FindByID( gems[ 'amethyst' ].itemID, 0x0000, containerID )
Items.Move( amethyst, containerID, 0, 29, 13 )
Misc.Pause( 700 )

citrine = Items.FindByID( gems[ 'citrine' ].itemID, 0x0000, containerID )
Items.Move( citrine, containerID, 0, 34, 13 )
Misc.Pause( 700 )

diamond = Items.FindByID( gems[ 'diamond' ].itemID, 0x0000, containerID )
Items.Move( diamond, containerID, 0, 51, 13 )
Misc.Pause( 700 )

emerald = Items.FindByID( gems[ 'emerald' ].itemID, 0x0000, containerID )
Items.Move( emerald, containerID, 0, 72, 13 )
Misc.Pause( 700 )

rubies = Items.FindByID( gems[ 'rubies' ].itemID, 0x0000, containerID )
Items.Move( rubies, containerID, 0, 81, 13 )
Misc.Pause( 700 )

sapphire = Items.FindByID( gems[ 'sapphire' ].itemID, 0x0000, containerID )
Items.Move( sapphire, containerID, 0, 88, 13 )
Misc.Pause( 700 )

starSapphire = Items.FindByID( gems[ 'star sapphire' ].itemID, 0x0000, containerID )
Items.Move( starSapphire, containerID, 0, 87, 11 )
Misc.Pause( 700 )

tourmaline = Items.FindByID( gems[ 'tourmaline' ].itemID, 0x0000, containerID )
Items.Move( tourmaline, containerID, 0, 125, 13 )
Misc.Pause( 700 )
