const treeId = window.SELECTED_TREE_ID;
fetch(`/tree/cytoscape?tree_id=${treeId}`) // pobiera dane z /tree/cytoscape -> 23 linijka w app.py, zwraca załadowane dane z pliku json
  .then(res => res.json()) // odczytuje odpowiedź jako json (Response zwrócone z get_tree())
  .then(data => { // data to sparsowany obiekt js czyli nasze drzewko
    const cy = cytoscape({
    container: document.getElementById('cy'), // rysuje drzewko w tym kontenerze (divie o id='cy', jest w tree.html)
    elements: [...data.nodes, ...data.edges], // łączy te dwie listy, żeby węzły i połączenia były razem
    style: [
      {
        selector: 'node', // styl dla każdego węzła
        style: {
          'shape': 'roundrectangle',
          'label': 'data(label)',
          'text-wrap': 'wrap',
          'text-max-width': 100,
          'padding': '10px',
          'color': '#fff',
          'text-valign': 'center',
          'text-halign': 'center',
          'text-outline-color': '#222',
          'text-outline-width': 2,
          'font-size': 12
        }
      },
      {
        selector: 'node[status = 0]', // styl dla niezrobionego zadania
        style: {
          'background-color': 'rgb(88, 88, 88)'
          }
      },
      {
        selector: 'node[status = 1]', // styl dla zrobionego ale niezaakceptowanego zadania
        style: {
          'background-color': 'rgb(177, 168, 99)'
        }
      },
      {
        selector: 'node[status = 2]', // styl dla zaakceptowanego zadania
        style: {
          'background-color': 'rgb(88, 159, 81)'
        }
      },
      {
        selector: 'edge', // styl dla gałęzi (strzałek basically)
        style: {
          'width': 2,
          'line-color': '#bbb',
          'target-arrow-shape': 'triangle',
          'target-arrow-color': '#bbb',
          'curve-style': 'bezier'
        }
      }
    ],

    layout: { // umieszczenie węzłów
      name: 'breadthfirst',
      directed: true,
      padding: 10
    },

    autoungrabify: true, //zeby uzytkownik nie mogl ruszac nodami
  });

  cy.userZoomingEnabled(false);
  cy.userPanningEnabled(false);
  cy.boxSelectionEnabled(false);

  const cyContainer = cy.container();

  //funkcja pan z ograniczeniem zeby nie wyjechac poza graf
  function clampPan(pan, bbox, container) {
    const containerHeight = container.clientHeight;
    const graphHeight = bbox.h;
    let minY, maxY;
    let margin = 16;
    if (graphHeight < containerHeight) {
      minY = maxY = (containerHeight - graphHeight) / 2 - bbox.y1; //jesli graf jest mniejszy od widoku jest wysrodkowany
    } else {
      minY = containerHeight - bbox.y2 - margin;
      maxY = -bbox.y1 + margin;
    }
    const clampedY = Math.max(minY, Math.min(maxY, pan.y));
    return { x: pan.x, y: clampedY };
  }

  //ustawianie scrollowania w myszce
  cyContainer.addEventListener('wheel', function(e) {
    if (e.deltaY !== 0) {
      e.preventDefault();
      document.querySelectorAll('.popper-div').forEach(e => e.remove()); //usuwa opisy, bo na razie nie ruszaja sie po pojawieniu
      const pan = cy.pan();
      const bbox = cy.elements().boundingBox();
      const container = cy.container();
      let newPan = { x: pan.x, y: pan.y - e.deltaY };
      newPan = clampPan(newPan, bbox, container);
      cy.pan(newPan);
    }
  }, { passive: false });

  cy.ready(() => {
    //ustawienie odpowiedniego poczatkowego zoom i pan
    const firstNode = cy.nodes()[0]; // zaklada ze pierwszy node bedzie pierwszy na liscie

    if (firstNode) {

      cy.zoom(1);
      cy.center(firstNode);

      const firstNodePos = firstNode.renderedPosition();
      const firstNodeHeight = firstNode.renderedHeight();
      const pxFromTop = 16;
      const offset = pxFromTop + firstNodeHeight/2 - firstNodePos.y;

      cy.panBy({x: 0, y: offset})
    }
  });

  function makeDiv(node) {
    let div = document.createElement('div');
    div.classList.add('popper-div');
    let html = `<div style="margin-bottom:8px; text-align:center;">${node.data('description') || 'Brak opisu'}</div>`;
    let buttonClass = '';
    let buttonText = '';
    let buttonHandler = null;
    let isDisabled = false;

    let baseClasses = "px-4 py-2 rounded-xl text-lg transition-colors duration-200";
    let statusClasses = "";
    let textColor = "text-black";

    switch (node.data('status')) {
        case 0:
            buttonClass = 'button btn-incomplete';
            buttonText = 'Oznacz jako wykonane';
            textColor = "text-green"
            buttonHandler = function() {
              console.log('Zaznaczone: ', node.data('id')) //placeholder
            };
            break;
        case 1:
            buttonClass = 'button btn-complete';
            buttonText = 'Wykonane';
            statusClasses = "bg-green-600 hover:bg-green-700";
            buttonHandler = function() {
                console.log('Odznaczone: ', node.data('id')) //placeholder
            };
            break;
        case 2:
            buttonClass = 'button btn-accepted';
            buttonText = 'Zatwierdzone';
            statusClasses = "bg-blue-600 opacity-70 cursor-default";
            isDisabled = true;
            break;
    }

    let disabledAttr = isDisabled ? "disabled" : "";
    html += `<button class="${baseClasses} ${statusClasses} ${textColor}" type="button" ${disabledAttr}>${buttonText}</button>`;

    div.innerHTML = html;
    document.body.appendChild(div);

    if (buttonHandler) {
        div.querySelector('button').addEventListener('click', buttonHandler);
    }

    return div;
  }

  cy.on('tap', 'node', function(evt) {
    document.querySelectorAll('.popper-div').forEach(e => e.remove());
    let node = evt.target;
    node.popper({
      content: function(){
        return makeDiv(node);
      }
    });
  });

  // cy.on('tap', function(evt) {
  //   if (evt.target === cy) {
  //     document.querySelectorAll('.popper-div').forEach(e => e.remove());
  //   }
  // });
});
