await figma.loadAllPagesAsync(); return figma.root.children.map(p => p.name + ' | ' + p.children.map(c => c.type + ':' + c.name).slice(0,3).join(', '));
