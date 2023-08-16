/** @type {import('./$types').PageLoad} */

export async function load({ fetch, setHeaders, params }) {
  let url = 'http://127.0.0.1:8000/api/products/'+params.slug
  const response = await fetch(url, {
            method: 'GET',
            headers: {
                'content-type': 'application/json'
            }
  });

  const posts = await response.json();
  // console.log(posts.results)
  return posts
}