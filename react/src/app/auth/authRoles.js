//src/app/authRoles.js
export const authRoles = {
  sa: ["SA"], // Only Super Admin has access
  admin: ["SA", "ADMIN"], // Only SA & Admin has access
  pro: ["SA", "ADMIN", "PRO"], // User acess PRO and above
  basic: ["SA", "ADMIN", "PRO", "BASIC"], // User acess BASIC and above
  free: ["SA", "ADMIN", "PRO", "BASIC", "FREE"], //  User acess FREE and above
  guest: ["SA", "ADMIN", "PRO", "BASIC", "FREE", "GUEST"] // Everyone has access
};
