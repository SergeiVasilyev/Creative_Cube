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
    <div class="photo_wrap">
        <Mygallery2 img_height='25rem' img_width='25rem' products={images} />
        <div>
            <p><b>Description: </b>{data.description}</p>
            <p><b></b><span class="price">€ {data.price - 2}.00</span><span class="normal_price ms-5">€ {data.price}</span></p>
            <p><b>Available: </b>{data.quantity}</p>
        </div>
    </div>
    
    
    <p>Tag: {data.tag = data.tag ? data.tag : ''}</p>
</div>


<style>
    .content {
        margin: 0 auto;
        padding: 2rem 2rem;
        max-width: 50%;
        border: 1px solid #ccc;
    }
    .photo_wrap {
        display: grid;
        margin-top: 15px;
        margin-bottom: 15px;
        grid-template-columns: auto auto;
        gap: 20px;
        /* border: 1px solid red; */
    }
    p {
        margin-bottom: 10px;
    }
    .price {
        font-size: 2.5rem;
        font-weight: 700;
    }
    .normal_price {
        text-decoration: line-through;
        font-size: 1.5rem;
        font-weight: 400;
    }
    img {
        width: 50%;
        height: auto;
    }
</style>