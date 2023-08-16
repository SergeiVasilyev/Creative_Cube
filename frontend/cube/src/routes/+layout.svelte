<script>
  import { page } from '$app/stores'
  import "../app.css"
  import Navbar from '../components/navbar.svelte'
  
</script>

<svelte:head>
  <title>{$page.data.title}</title>
</svelte:head>

<Navbar />

<main class="pb-9">
  <slot></slot>
</main>
  

<style>
</style>
