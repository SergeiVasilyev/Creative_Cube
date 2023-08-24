<script>
    /** @type {import('./$types').PageData} */
    export let data
    import Mygallery2 from '../../../components/mygallery2.svelte'

    console.log(data)

    let images = []
    data.images.forEach(item => {
        images.push(item.img_name)
    })
    console.log(images)
</script>

<svelte:head>
  <title>{data.name}</title>
</svelte:head>


<div class="content">
    <h1>{data.name}</h1>
    <!-- {#each data.images as image}
    <img src="http://127.0.0.1:8000/{image.img_name}" alt={image.img_name} />
    {/each} -->
    <Mygallery2 img_height='30vw' products={images} />
    <p>{data.description}</p>
    <p>Price: {data.price}</p>
    <p>Quantity: {data.quantity}</p>
    <p>Tag: {data.tag = data.tag ? data.tag : ''}</p>
</div>


<style>
    .content {
        margin: 0 auto;
        padding: 2rem 2rem;
        max-width: 50%;
    }
    img {
        width: 50%;
        height: auto;
    }
</style>