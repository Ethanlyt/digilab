"use client";

import { useState, useMemo } from "react";

type Post = {
	id: number;
	title: string;
};

export default function PostsClient({ posts }: { posts: Post[] }) {
	const [search, setSearch] = useState("");

	const filteredPosts = useMemo(() => {
		return posts.filter((post) =>
			post.title.toLowerCase().includes(search.toLowerCase())
		);
	}, [search, posts]);

	return (
		<>
			<input
				type='text'
				placeholder='Search by title...'
				value={search}
				onChange={(e) => setSearch(e.target.value)}
				style={{
					padding: "0.5rem",
					width: "300px",
					marginBottom: "1rem",
				}}
			/>

			<ul>
				{filteredPosts.map((post) => (
					<li key={post.id}>{post.title}</li>
				))}
			</ul>
		</>
	);
}
