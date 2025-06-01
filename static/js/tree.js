fetch('/tree/cytoscape') // pobiera dane z /tree/cytoscape -> 23 linijka w app.py, zwraca załadowane dane z pliku json
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

    autoungrabify: true,
  });

  cy.ready(() => {
    //ustawienie odpowiedniego poczatkowego zoom i pan
    const firstNode = cy.nodes()[0]; // zaklada ze pierwszy node bedzie pierwszy na liscie

    if (firstNode) {

      cy.zoom(1);
      cy.center(firstNode);

      const firstNodePos = firstNode.renderedPosition();
      const firstNodeHeight = firstNode.renderedHeight();
      const pxFromTop = 0; // poczatkowo mialo byc okreslona ilosc px z gory, teraz robione wzgledem wysokosci noda
      const offset = pxFromTop + firstNodeHeight - firstNodePos.y;

      cy.panBy({x: 0, y: offset})
    }
  });

  function makeDiv(text) {
    var div = document.createElement('div');
    div.classList.add('popper-div');
    div.innerHTML = text;
    document.body.appendChild(div);
    return div;
  }

  cy.on('tap', 'node', function(evt) {
    document.querySelectorAll('.popper-div').forEach(e => e.remove());
    var node = evt.target;
    node.popper({
      content: function(){
        return makeDiv(node.data('description') || 'Brak opisu');
      }
    });
  });

  cy.on('tap', function(evt) {
    if (evt.target === cy) {
      document.querySelectorAll('.popper-div').forEach(e => e.remove());
    }
  });
});
