await figma.loadAllPagesAsync();
return {sets: figma.root.findAllWithCriteria({types: ["COMPONENT_SET"]}).length, pages: figma.root.children.length};
