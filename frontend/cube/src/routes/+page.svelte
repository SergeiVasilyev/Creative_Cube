<script>
    import Card from '../components/card.svelte'
    import Mygallery from "../components/mygallery.svelte"
    /** @type {import('./$types').PageData} */
    export let data

</script>



<div class="container">
    <h1 class="mb-4 mt-5">Last products</h1>
    <div class="gallary_wrap">
        <Mygallery img_height='30vw' products={data.results} />
    </div>
    <h1 class="pt-9 ml-8">Our Products</h1>
    <div class="cat">
        {#each data.results as product}
            <Card header={product.name} 
                description={product.description} 
                price={product.price} 
                src={product.images[0] ? product.images[0].img_name : ''} 
                product_id={product.id} 
                product_slug={product.slug}/>
        {/each}
    </div>
</div>

<style>
    .gallary_wrap {
        margin: 0 auto;
        max-width: 100%;
    }
    .container {
        margin: 0 auto;
        padding: 0 2rem;
        max-width: 90%;
    }
    .cat {
        display: grid;
        justify-content: center;
        grid-template-columns: repeat(auto-fit, 318px);
        gap: 20px;
        margin-top: 20px;
    }
</style>

