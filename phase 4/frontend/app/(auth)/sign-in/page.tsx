import AuthForm from "@/components/AuthForm";

export default function SignInPage() {
  return (
    <div className="min-h-screen bg-auth-mesh flex items-center justify-center px-4">
      <AuthForm mode="sign-in" />
    </div>
  );
}
