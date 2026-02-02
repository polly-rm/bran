document.getElementById('dynamicModal')
    .addEventListener('show.bs.modal', function (event) {

        const trigger = event.relatedTarget;

        const title = trigger.getAttribute('data-title');
        const weight = trigger.getAttribute('data-weight');
        const size = trigger.getAttribute('data-size');
        const info = trigger.getAttribute('data-info');

        this.querySelector('#modalTitle').textContent = title;
        this.querySelector('#modalWeight').textContent = weight;
        this.querySelector('#modalSize').textContent = size;

        if (info) {
            this.querySelector('#modalInfo').textContent = info;
        }

        const time = title === 'Small Van' ? '10' : '15';

        this.querySelectorAll('.modalTime').forEach(span => {
            span.textContent = time;
        });
    });