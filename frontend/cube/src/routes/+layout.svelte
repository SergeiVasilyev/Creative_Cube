<script>
  import { page } from '$app/stores'
  import "../app.css"
  import Navbar from '../components/navbar.svelte'
  
</script>



<Navbar />

<main class="pb-9">
  <slot></slot>
</main>
  

<style>
</style>
