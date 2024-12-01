"use client";

import { useState, useEffect } from "react";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import {
  User,
  Mail,
  Lock,
  Calendar,
  Transgender,
  Image as ImageIcon,
  Save,
  Loader2,
} from "lucide-react";
import Link from "next/link";
import { signOut } from "next-auth/react";
import { toast } from "sonner";

export default function ProfilePage() {
  const [userData, setUserData] = useState({
    name: "",
    email: "",
    age: "",
    gender: "",
    image: "",
  });
  const [isEditing, setIsEditing] = useState(false);
  const [isLoading, setIsLoading] = useState(true);

  // Fetch user data
  useEffect(() => {
    const fetchUserData = async () => {
      try {
        const response = await fetch("/api/profile");
        if (!response.ok) {
          throw new Error("Failed to fetch user data");
        }
        const data = await response.json();
        setUserData(data.user);
        setIsLoading(false);
      } catch (error) {
        console.error("Error fetching user data:", error);
        toast.error("Failed to load profile data");
        setIsLoading(false);
      }
    };

    fetchUserData();
  }, []);

  // Handle input changes
  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setUserData((prev) => ({
      ...prev,
      [name]: value,
    }));
  };

  // Save profile changes
  const handleSaveProfile = async () => {
    try {
      const response = await fetch("/api/profile", {
        method: "PUT",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(userData),
      });

      if (!response.ok) {
        throw new Error("Failed to update profile");
      }

      const data = await response.json();
      setUserData(data.user);
      setIsEditing(false);
      toast.success("Profile updated successfully");
    } catch (error) {
      console.error("Error updating profile:", error);
      toast.error("Failed to update profile");
    }
  };

  if (isLoading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <Loader2 className="w-12 h-12 animate-spin text-primary" />
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-background via-background to-primary/5">
      <header className="border-b">
        <div className="container px-4 py-4 mx-auto">
          <nav className="flex items-center justify-between">
            <Link href="/dashboard" className="text-2xl font-bold">
              Burnout Predictor
            </Link>
            <div className="flex items-center space-x-4">
              <Button variant="ghost" asChild>
                <Link href="/dashboard/health-data">Health Data</Link>
              </Button>
              <Button variant="ghost" asChild>
                <Link href="/dashboard/profile">Profile</Link>
              </Button>
              <Button
                variant="destructive"
                onClick={() => signOut({ redirectTo: "/" })}
              >
                Sign Out
              </Button>
            </div>
          </nav>
        </div>
      </header>

      <main className="container max-w-2xl p-4 mx-auto">
        <Card className="mt-8 overflow-hidden transition-shadow duration-300 shadow-lg hover:shadow-xl">
          <CardHeader className="bg-primary/5">
            <CardTitle className="flex items-center space-x-2 text-2xl font-bold">
              <User className="w-6 h-6 text-primary" />
              <span>My Profile</span>
            </CardTitle>
          </CardHeader>
          <CardContent className="p-6 space-y-6">
            <div className="grid gap-4 md:grid-cols-2">
              <div>
                <Label className="flex items-center space-x-2">
                  <User className="w-4 h-4 text-muted-foreground" />
                  <span>Name</span>
                </Label>
                {isEditing ? (
                  <Input
                    name="name"
                    value={userData.name || ""}
                    onChange={handleInputChange}
                    placeholder="Enter your name"
                  />
                ) : (
                  <p className="p-2 rounded bg-accent/50">
                    {userData.name || "Not provided"}
                  </p>
                )}
              </div>
              <div>
                <Label className="flex items-center space-x-2">
                  <Mail className="w-4 h-4 text-muted-foreground" />
                  <span>Email</span>
                </Label>
                {isEditing ? (
                  <Input
                    name="email"
                    value={userData.email || ""}
                    onChange={handleInputChange}
                    placeholder="Enter your email"
                    type="email"
                  />
                ) : (
                  <p className="p-2 rounded bg-accent/50">
                    {userData.email || "Not provided"}
                  </p>
                )}
              </div>
              <div>
                <Label className="flex items-center space-x-2">
                  <Calendar className="w-4 h-4 text-muted-foreground" />
                  <span>Age</span>
                </Label>
                {isEditing ? (
                  <Input
                    name="age"
                    value={userData.age || ""}
                    onChange={handleInputChange}
                    placeholder="Enter your age"
                    type="number"
                  />
                ) : (
                  <p className="p-2 rounded bg-accent/50">
                    {userData.age || "Not provided"}
                  </p>
                )}
              </div>
              <div>
                <Label className="flex items-center space-x-2">
                  {/* <Transgender className="w-4 h-4 text-muted-foreground" /> */}
                  <span>Gender</span>
                </Label>
                {isEditing ? (
                  <select
                    name="gender"
                    value={userData.gender || ""}
                    onChange={handleInputChange}
                    className="w-full p-2 border rounded"
                  >
                    <option value="">Select Gender</option>
                    <option value="male">Male</option>
                    <option value="female">Female</option>
                  </select>
                ) : (
                  <p className="p-2 rounded bg-accent/50">
                    {userData.gender || "Not provided"}
                  </p>
                )}
              </div>
            </div>

            <div>
              <Label className="flex items-center mb-2 space-x-2">
                <ImageIcon className="w-4 h-4 text-muted-foreground" />
                <span>Profile Image URL</span>
              </Label>
              {isEditing ? (
                <Input
                  name="image"
                  value={userData.image || ""}
                  onChange={handleInputChange}
                  placeholder="Enter image URL"
                />
              ) : (
                <div className="flex items-center space-x-4">
                  {userData.image ? (
                    <img
                      src={userData.image}
                      alt="Profile"
                      className="object-cover w-24 h-24 rounded-full"
                    />
                  ) : (
                    <p className="p-2 rounded bg-accent/50">No profile image</p>
                  )}
                </div>
              )}
            </div>

            <div className="flex justify-end space-x-4">
              {isEditing ? (
                <>
                  <Button variant="outline" onClick={() => setIsEditing(false)}>
                    Cancel
                  </Button>
                  <Button
                    onClick={handleSaveProfile}
                    className="flex items-center space-x-2"
                  >
                    <Save className="w-4 h-4" />
                    <span>Save Changes</span>
                  </Button>
                </>
              ) : (
                <Button onClick={() => setIsEditing(true)} variant="secondary">
                  Edit Profile
                </Button>
              )}
            </div>
          </CardContent>
        </Card>
      </main>
    </div>
  );
}
