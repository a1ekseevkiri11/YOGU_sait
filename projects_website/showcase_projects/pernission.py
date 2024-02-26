def canAddProject(user):
    return user.has_perm('showcase_projects.add_project')


def canAddParticipation(user):
    return user.has_perm('showcase_projects.add_participation')