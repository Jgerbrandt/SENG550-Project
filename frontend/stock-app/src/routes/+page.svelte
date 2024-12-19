<script lang="ts">
    import { onMount } from 'svelte';
    import PocketBase from 'pocketbase';
    import { Chart, registerables } from 'chart.js';

    const pb = new PocketBase('http://127.0.0.1:8090');
    Chart.register(...registerables);

    let item: { ml: any[], actual: any[] } = { ml: [], actual: [] };

	let chart_context: any;
	let chart_canvas: any;

    // Fetch initial data from the collection
    async function fetchData() {
        try {
            const result = await pb.collection('AMZN').getList(1, 1, {});
            console.log('Fetched data:', result);
            if (result.items.length > 0) {
                const fetchedItem = result.items[0];
                item = {
                    ml: fetchedItem.ml,
                    actual: fetchedItem.actual
                };
            }
        } catch (error) {
            console.error('Error fetching data:', error);
        }
    }

    onMount(() => {
        fetchData();

        // Subscribe to the collection
        pb.collection('AMZN').subscribe('*', function (e: any) {
            console.log('Subscription event:', e);
            const updatedItem = e.record;
            item = {
                ml: updatedItem.ml,
                actual: updatedItem.actual
            };
        }).catch((error: any) => {
            console.error('Error subscribing to collection:', error);
        });

		chart_context = chart_canvas.getContext('2d');
            var chart = new Chart(chart_context, {
				type: 'line',
				data: {
						labels: ['a', 'b', 'c', 'd', 'e', 'f', 'g'],
						datasets: [{
								label: 'Revenue',
								backgroundColor: 'rgb(255, 99, 132)',
								borderColor: 'rgb(255, 99, 132)',
								data: [0, 10, 5, 2, 20, 30, 45],
						}]
				}
		});

    });

</script>

<main>
    <h1>Item</h1>
    <div>
        <div>ML: {item.ml}</div>
        <div>Actual: {item.actual}</div>
    </div>
	
	<canvas bind:this={chart_canvas} id="myChart"></canvas>

</main>