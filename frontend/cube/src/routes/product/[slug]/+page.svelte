<script>
    /** @type {import('./$types').PageData} */
    export let data
    console.log(data)
</script>

<svelte:head>
  <title>{data.name}</title>
</svelte:head>

<h1>{data.name}</h1>
<div>
    {#each data.images as image}
    <img src="http://127.0.0.1:8000/{image.img_name}" alt={image.img_name} />
    {/each}
    <p>{data.description}</p>
    <p>Price: {data.price}</p>
    <p>Quantity: {data.quantity}</p>
    <p>Tag: {data.tag = data.tag ? data.tag : ''}</p>
</div>


<style>
    img {
        width: 20%;
        height: auto;
    }
</style>