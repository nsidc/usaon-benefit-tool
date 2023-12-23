---
title: "Releasing"
---

"Releasing" means sharing a completed code package to the world. It does not mean
running that code package! That would be "deployment", and can look different depending
on who is doing the deployment on on to what system.


## CHANGELOG

Author a new changelog section titled `NEXT_VERSION`. The `bump-my-version` step will
replace this magic string with a correct version identification.


## Bump the version

This application users [semver](https://semver.org).

The version number must be updated in many places, so we use `bump-my-version` to
automate the process. To increase the minor version number:

```bash
bump-my-version bump minor
```


## Release

After everything is merged, create a release in the GitHub UI.

Releases that are labeled `alpha`, `beta`, or `rc` must be marked as
pre-releases.

After the release is created, GitHub Actions will start building the container images.
Once GitHub Actions is done, you can deploy the app with the deploy script
(`deploy/deploy`).

> [!NOTE]
>
> At NSIDC, this deployment should be done with _Garrison_ after automations have
> successfully completed.


### Automations

This will trigger [GitHub Actions](https://github.com/nsidc/usaon-benefit-tool/actions)
to release new container images to Docker Hub and GitHub Packages. It should take at
most 5-10 minutes.

The ReadTheDocs `stable` page will also automatically update.
