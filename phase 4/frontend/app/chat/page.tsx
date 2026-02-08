import { headers } from "next/headers";
import { redirect } from "next/navigation";
import { auth } from "@/lib/auth";
import Navbar from "@/components/Navbar";
import ChatInterface from "@/components/ChatInterface";

export default async function ChatPage() {
  const session = await auth.api.getSession({ headers: await headers() });

  if (!session) {
    redirect("/sign-in");
  }

  return (
    <div className="min-h-screen bg-mesh">
      <Navbar userName={session.user.name} />
      <ChatInterface />
    </div>
  );
}
