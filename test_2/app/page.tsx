import PostsClient from "./posts-client";

export default async function HomePage() {
	const res = await fetch(
		"https://jsonplaceholder.typicode.com/posts",
		{ cache: "no-store" } // SSR
	);

	const posts = await res.json();

	return (
		<main style={{ padding: "2rem" }}>
			<h1>Posts</h1>
			<PostsClient posts={posts} />
		</main>
	);
}