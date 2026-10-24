const mathContent = document.querySelector('.post-content');
if (mathContent && typeof renderMathInElement === 'function') {
    renderMathInElement(mathContent, {
        delimiters: [
            { left: '$$', right: '$$', display: true },
            { left: '\\[', right: '\\]', display: true },
            { left: '\\(', right: '\\)', display: false },
            { left: '$', right: '$', display: false }
        ],
        throwOnError: false,
        trust: false
    });
}
