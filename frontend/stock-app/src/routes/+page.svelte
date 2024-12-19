<script lang="ts">
    import { onMount } from 'svelte';
    import PocketBase from 'pocketbase';
    import { Chart, registerables } from 'chart.js';

    const pb = new PocketBase('http://127.0.0.1:8090');
    Chart.register(...registerables);

    let item: { ml: any[], actual: any[] } = { ml: [], actual: [] };

	let chart: any;
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

	function updateChart() {
        if (chart) {
            chart.data.labels = Array.from({ length: item.ml.length }, (_, i) => i + 1);
            chart.data.datasets[0].data = item.ml;
            chart.data.datasets[1].data = item.actual;
            chart.update();
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
            updateChart();
        }).catch((error: any) => {
            console.error('Error subscribing to collection:', error);
        });

        chart_context = chart_canvas.getContext('2d');
        chart = new Chart(chart_context, {
            type: 'line',
            data: {
                labels: [], // Initial empty labels
                datasets: [
                    {
                        label: 'ML',
                        backgroundColor: 'rgba(75, 192, 192, 0.2)',
                        borderColor: 'rgba(75, 192, 192, 1)',
                        data: [], // Initial empty data
                    },
                    {
                        label: 'Actual',
                        backgroundColor: 'rgba(255, 99, 132, 0.2)',
                        borderColor: 'rgba(255, 99, 132, 1)',
                        data: [], // Initial empty data
                    }
                ]
            },
            options: {
                responsive: true,
				animation: false,
                scales: {
                    x: {
                        display: true,
                        title: {
                            display: true,
                            text: 'Index',
                            color: 'white' // White text
                        },
                        ticks: {
                            color: 'white' // White text
                        },
                        grid: {
                            color: 'rgba(255, 255, 255, 0.2)' // White grid lines
                        }
                    },
                    y: {
                        display: true,
                        title: {
                            display: true,
                            text: 'Value',
                            color: 'white' // White text
                        },
                        ticks: {
                            color: 'white' // White text
                        },
                        grid: {
                            color: 'rgba(255, 255, 255, 0.2)' // White grid lines
                        },
                    },
                },
				plugins: {}
            },
			plugins: [{
                id: 'background',
                beforeDraw: (chart) => {
                    const ctx = chart.canvas.getContext('2d');
                    if (ctx) {
                        ctx.save();
                        ctx.globalCompositeOperation = 'destination-over';
                        ctx.fillStyle = 'rgba(0, 0, 0, 0.5)'; // Slightly darker background
                        ctx.fillRect(0, 0, chart.width, chart.height);
                        ctx.restore();
                    }
                }
            }]
        });
    });
</script>

<style>

    .chart-container {
        display: flex;
        justify-content: center;
        align-items: center;
        height: 100vh;
    }

    .chart-wrapper {
        width: 80%;
        height: 70%;
        background-color: rgba(0, 0, 0, 0.7);
        padding: 20px;
        border-radius: 10px;
    }

    canvas {
        width: 100% !important;
        height: 100% !important;
    }
</style>

<main>
    <div class="chart-container">
        <div class="chart-wrapper">
            <canvas bind:this={chart_canvas} id="myChart"></canvas>
        </div>
    </div>
</main>