<script lang="ts">
    import { onMount } from 'svelte';
    import PocketBase from 'pocketbase';

    const pb = new PocketBase('http://127.0.0.1:8090');

    let item: { ml: any, actual: any } = { ml: null, actual: null };

    // Fetch initial data
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
    });
</script>

<main>
    <h1>Item</h1>
    <div>
        <div>ML: {item.ml}</div>
        <div>Actual: {item.actual}</div>
    </div>
</main>