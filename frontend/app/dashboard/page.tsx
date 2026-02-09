import { headers } from "next/headers";
import { redirect } from "next/navigation";
import { auth } from "@/lib/auth";
import Navbar from "@/components/Navbar";
import TaskList from "@/components/TaskList";

export default async function DashboardPage() {
  try {
    const session = await auth.api.getSession({ headers: await headers() });

    if (!session) {
      redirect("/sign-in");
    }

    return (
      <div className="min-h-screen bg-mesh">
        <Navbar userName={session.user.name} />
        <main className="max-w-6xl mx-auto px-4 py-8">
          <TaskList />
        </main>
      </div>
    );
  } catch (error) {
    console.error("Dashboard session error:", error);
    redirect("/sign-in");
  }
}
