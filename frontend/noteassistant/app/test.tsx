import React from 'react';
import Mermaid from 'react-mermaid2';

const MermaidDiagram = () => {
  const diagram = `
    graph TD;
      A-->B;
      A-->C;
      B-->D;
      C-->D;
  `;

  return (
    <div>
      <Mermaid chart={diagram} />
    </div>
  );
};

export default MermaidDiagram;
