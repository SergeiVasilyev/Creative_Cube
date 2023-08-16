<script>
    export let src = "https://www.topgear.com/sites/default/files/2022/07/6_0.jpg"
    export let header = ''
    export let description = ''
    export let price = ''
    export let product_slug = ''
    export let product_id

    let heart = 'm8 2.748-.717-.737C5.6.281 2.514.878 1.4 3.053c-.523 1.023-.641 2.5.314 4.385.92 1.815 2.834 3.989 6.286 6.357 3.452-2.368 5.365-4.542 6.286-6.357.955-1.886.838-3.362.314-4.385C13.486.878 10.4.28 8.717 2.01L8 2.748zM8 15C-7.333 4.868 3.279-3.04 7.824 1.143c.06.055.119.112.176.171a3.12 3.12 0 0 1 .176-.17C12.72-3.042 23.333 4.867 8 15z'
    let heart_filled = 'M8 1.314C12.438-3.248 23.534 4.735 8 15-7.534 4.736 3.562-3.248 8 1.314z'
    let heart_chacked = false

    function btn_click() {
        heart_chacked = !heart_chacked
    }


    $: newHedaer = header

    /**
	 * @param {HTMLInputElement} element
	 * @param {{ (): void; (): void; }} callbackFunction
	 */
    function handleClickOutside(element, callbackFunction){
        console.log('clicked outside', element)
        /**
		 * @param {{ target: any; }} event
		 */
        function onClick(event) {
            // console.log(element.contains, event.target)
			if (!element.contains(event.target)) {
				callbackFunction();
                console.log(newHedaer, src)
			}
		}
		
		document.body.addEventListener('click', onClick)
        return {
			/**
			 * @param {any} newCallbackFunction
			 */
			update(newCallbackFunction) {
				callbackFunction = newCallbackFunction;
			},
			destroy() {
				document.body.removeEventListener('click', onClick);
			}
		}
    }
    let showModal = false;

</script>

<div class="card_cont">
    <a data-sveltekit-preload-data="tap" href="/products/{product_slug}">
        <img class="mb-5" src={src} alt={src} />
    </a>

    <div class="flex justify-between">
        {#if !showModal} <!-- TODO: add: if user is staff -->
        <a href={'#'} class="h3_container" on:click={(event) => {event.preventDefault(); showModal = true; event.stopPropagation();}}>
            <h3 class="">{newHedaer}</h3>
        </a>
        {:else}
        <input type="text" bind:value={header} use:handleClickOutside={() => {console.log('clicked outside'); showModal = false;}} />
        {/if}

        <div>
            <button on:click={btn_click}>
                <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-heart" viewBox="0 0 16 16">
                    {#if !heart_chacked}
                        <path d={heart}/>
                    {:else}
                        <path d={heart_filled}/>
                    {/if}
                </svg>
            </button>
        </div>
    </div>

    <p class="my-3">{description.slice(0, 65)}...</p>
    <p>{price}</p>
</div>

<style>
    .card_cont {
        padding: 0.5em;
        border: 1px solid #e4e4e4;
        background-color: white;
    }
    .card_cont h3 {
        font-weight: 600;
        padding: 0 0.5em;
        border: solid 1px white;
    }
    .card_cont input, .card_cont h3 {
        font-size: 1.4em;
    }
    .card_cont p {
        padding: 0.01em 0.5em;
        /* border: solid 1px white; */
    }
    img {
        max-width: 300px;
    }
</style>

