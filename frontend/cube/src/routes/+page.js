/** @type {import('./$types').PageLoad} */

export async function load({ fetch, setHeaders }) {
  const response = await fetch('http://127.0.0.1:8000/api/products/', {
            method: 'GET',
            headers: {
                'content-type': 'application/json'
            }
  });

  const data = await response.json()
  console.log(data)

  return data
}
