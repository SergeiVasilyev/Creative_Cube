<!-- Opacity -->
<script>
    import { onMount } from 'svelte';
    /**
	 * @type {string | any[]}
	 */
    export let products = []
    export let img_height = '50vh'


    /**
	 * @type {string | any[]}
	 */
    let slides = []
    let slideIndex = 0
    onMount(() => {
        setImage(0)
    })

    /**
	 * @param {number} n
	 */
    function plusSlides(n) {
        slideIndex += n
        slideIndex = setImage(slideIndex)
    }
    
    /**
	 * @param {number} n
	 */
    function currentSlide(n) {
		slideIndex = setImage(n)
    }
    
    /**
	 * @param {number} n
	 */
    function setImage(n) {
        console.log('setImage: ', n)
        slideIndex = checkIndex(n)
        console.log('slideIndex: ', slideIndex)
        for (let i = 0; i < slides.length; i++) {
            slides[i].style.opacity = '0'
        }

        slides[slideIndex].style.opacity  = '1'
        return slideIndex
    }

    /**
	 * @param {number} n
	 */
    function checkIndex(n) {
        let x = n
        console.log('products.length: ', products.length)
        if (n > products.length-1) {x = 0}
        if (n < 0) {x = products.length-1}
        console.log('slideIndex x: ', x)
        return x
    }

</script>

<slot name="slideshow-container">
    <div class="slideshow-container" style="height:{img_height}">
        {#each products as product, index}
            <div class="mySlides" bind:this={slides[index]}>
                <div class="numbertext">{index+1} / {products.length}</div>
                <img src="{product}" alt="{product}" style="height:{img_height}">
                <!-- <div class="text">{product.name}</div> -->
            </div>
        {/each}

        <a href={'#'} class="prev" on:click={(event) => {event.preventDefault(); plusSlides(-1);}}>&#10094;</a>
        <a href={'#'} class="next" on:click={(event) => {event.preventDefault(); plusSlides(1);}}>&#10095;</a>
        
        <div style="text-align:center" class="dot_wrap">
            {#each products as d, index}
                <button class="dot {slideIndex === index ? 'active' : ''}" on:click={(event) => {event.preventDefault(); currentSlide(index);}}></button>
            {/each}
        </div>
    </div>
</slot>


<style>
    * {
        box-sizing:border-box
    }

    img {
        width: 100%;
        object-fit: cover;
        object-position: 50% 50%;
    }

    .slideshow-container {
        position: relative;
        margin: auto;
    }

    .mySlides {
        position: absolute;
        width: 100%;
        opacity: 0;
        transition: opacity 1s ease-in-out;
    }

    .prev, .next {
        cursor: pointer;
        position: absolute;
        top: 50%;
        width: auto;
        margin-top: -22px;
        padding: 16px;
        color: white;
        font-weight: bold;
        font-size: 18px;
        transition: 0.6s ease;
        border-radius: 0 3px 3px 0;
        user-select: none;
        background-color: rgba(0,0,0,0.02);
        text-decoration: none;
    }

    .next {
        right: 0;
        border-radius: 3px 0 0 3px;
    }

    .prev:hover, .next:hover {
        background-color: rgba(0,0,0,0.8);
    }

    .text {
        color: #f2f2f2;
        text-shadow: 1px 1px 2px #535353;
        font-size: 15px;
        padding: 8px 12px;
        position: absolute;
        top: 0;
        width: 100%;
        text-align: center;
    }

    .dot_wrap{
        position: absolute;
        bottom: 2%;
        width: 100%;
        text-align: center;        
    }

    .numbertext {
        color: #f2f2f2;
        text-shadow: 1px 1px 2px #535353;
        font-size: 12px;
        padding: 8px 12px;
        position: absolute;
        top: 0;
    }

    .dot {
        cursor: pointer;
        height: 15px;
        width: 15px;
        margin: 0 4px;
        background-color: #ddd;
        border-radius: 50%;
        border: 0.3px solid rgba(0,0,0,0.2);
        display: inline-block;
        transition: background-color 0.6s ease;
    }

    .active, .dot:hover {
        background-color: #717171;
    }


</style>