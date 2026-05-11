export function getProfilePictureUrl(profilePicture) {
  if (!profilePicture) {
    return ''
  }

  if (/^https?:\/\//i.test(profilePicture)) {
    return profilePicture
  }

  return `/uploads/${profilePicture}`
}
