import mermaid from 'https://cdn.jsdelivr.net/npm/mermaid@12.2.0/dist/mermaid.esm.min.mjs';

const diagrams = Array.from(document.querySelectorAll('.mermaid'), node => ({
    node,
    source: node.textContent
}));
let renderId = 0;
let renderQueue = Promise.resolve();

async function renderDiagrams() {
    await document.fonts.ready;
    mermaid.initialize({
        startOnLoad: false,
        securityLevel: 'strict',
        theme: document.documentElement.dataset.theme === 'dark' ? 'dark' : 'default'
    });
    for (const { node, source } of diagrams) {
        const { svg, bindFunctions } = await mermaid.render(`diagram-${++renderId}`, source);
        node.innerHTML = svg;
        bindFunctions?.(node);
    }
}

function scheduleRender() {
    renderQueue = renderQueue.then(renderDiagrams).catch(error => {
        console.error('Mermaid diagram rendering failed:', error);
    });
}

scheduleRender();
new MutationObserver(scheduleRender).observe(document.documentElement, {
    attributes: true,
    attributeFilter: ['data-theme']
});
