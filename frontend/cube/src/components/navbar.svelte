<script>
    let show_nav
</script>

<header class="header flex justify-between px-5 py-5 shadow-md bg-white sticky top-0 z-50">
    <a href="/" class="logo text-4xl text-black-500 font-bold text-slate-900">Creative Box</a>
    <nav class="nav absolute flex flex-col shadow-md w-[50%] h-full right-0 bg-white px-4 md:static md:h-auto md:w-auto md:flex-row md:shadow-none duration-500">
      <button class="close-nav relative top-0 right-0 text-right text-3xl md:hidden">
        <i class="fa-solid fa-xmark"></i>
      </button>

      <a href={'/'} class="nav-link text-2xl mb-2 md:mr-9 hover:text-emerald-600">Home</a>
      <a href={'/products'} class="nav-link text-2xl mb-2 md:mr-9 hover:text-emerald-600">Products</a>
      <a href={'/about'} class="nav-link text-2xl mb-2 md:mr-9 hover:text-emerald-600">About</a>
      <a href={'/settings'} class="nav-link text-2xl mb-2 md:mr-9 hover:text-emerald-600">Settings</a>
    </nav>

    <button class="show-nav text-3xl cursor-pointer" bind:this="{show_nav}">
      <i class="fa-solid fa-bars"></i>
    </button>
</header>

<style>
    .logo {
        font-family: 'rubik';
    }
</style>