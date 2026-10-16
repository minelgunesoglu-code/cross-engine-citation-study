# Archiving this repository on Zenodo and minting a DOI

Everything in this file is a manual, ordered checklist for the repository owner.
Steps marked **[LOGIN]** happen inside an authenticated session on zenodo.org or
github.com and **cannot be automated from here**: an agent has no account and
must not create one. Steps marked **[LOCAL]** are ordinary git commands the owner
runs, or approves, on this machine.

The one-line summary: Zenodo watches for a **GitHub Release**, not for a tag, and
it only archives releases created **after** the repository has been switched on
in Zenodo. Get the order wrong and the release is simply ignored.

State on handover: the repository exists locally at `~/cross-engine-citation-study`. It has one commit on `main`.
Nothing has been pushed, no GitHub repository exists yet, and nothing has been
done on Zenodo.

---

## 0. Before anything: settle these

- **Site files.** Seven short notes in the June CSV and JSON were translated into
  English for this archive (`notes/reproduction-check.md` lists them). Apply the
  same seven changes to the site's copies so the two match.
- **Publication date.** `.zenodo.json` sets `"publication_date": "2026-06-19"`,
  the day round one was published on the site; round two was published on 9 August 2026, and `CITATION.cff` uses the same date. If the deposit date is
  preferred instead, change both.
- **Version and tag.** `.zenodo.json` says `"version": "1.0.0"` and the tag below
  is `v1.0.0`. They must not disagree.
- **Email in `CITATION.cff`.** It carries `minel@ismybrandinai.com`, as in the
  earlier deposits. Remove the line if the address should not appear in GitHub's
  citation box.

---

## 1. Create the GitHub repository **[LOGIN]**

On github.com, signed in as **minelgunesoglu-code**, create a new **public**
repository named exactly **`cross-engine-citation-study`**. Leave it empty: no README, no licence, no
`.gitignore`, because all of them already exist locally and a generated first
commit would conflict with the local history.

Or, if `gh` is already authenticated as `minelgunesoglu-code`:

```bash
gh repo create minelgunesoglu-code/cross-engine-citation-study --public \
  --description "Cross-Engine Citation Study, rounds one and two: data and method notes"
```

## 2. Push **[LOCAL]**

```bash
cd ~/cross-engine-citation-study
git remote add origin https://github.com/minelgunesoglu-code/cross-engine-citation-study.git
git push -u origin main
```

Check on github.com that `README.md` renders, and that `data/` holds four files.

---

## 3. Connect the GitHub account to Zenodo **[LOGIN]**

Skip this step if it was already done for an earlier study; the connection is per
account, not per repository.

1. Go to <https://zenodo.org> and sign in. Signing in **with GitHub** connects the
   two accounts in one action.
2. Authorise the Zenodo GitHub application when GitHub asks.
3. Confirm the connected account is **minelgunesoglu-code**.

## 4. Enable archiving for this repository **[LOGIN]**

From <https://help.zenodo.org/docs/github/enable-repository>:

1. Click the profile menu in the header and click **GitHub**.
2. Click **Sync now**.
3. Find **`minelgunesoglu-code/cross-engine-citation-study`** and toggle its slider on.
4. Refresh the page and check it is listed as enabled.

Checks worth making while there:

- The repository must be **public** and the account must have admin rights on it,
  or the toggle will not stick.
- If the repository is missing from the list, press **Sync now** again; a newly
  created repository can lag.
- Leave every other repository as it is. Do **not** enable `ismybrandinai-site` or
  any other private repository.

---

## 5. Create the release v1.0.0 **[LOCAL tag, LOGIN release]**

`.zenodo.json` is already in the initial commit, so it is in the tagged tree.
Zenodo reads it **from the tagged commit**, and when both `.zenodo.json` and
`CITATION.cff` exist it uses only `.zenodo.json`.

```bash
cd ~/cross-engine-citation-study
git tag -a v1.0.0 -m "Cross-Engine Citation Study, rounds one and two: 19 June and 6 to 7 August 2026"
git push origin v1.0.0
```

**Pushing the tag is not enough.** Turn it into a release:

- In the browser:
  <https://github.com/minelgunesoglu-code/cross-engine-citation-study/releases/new>
  → choose the tag `v1.0.0` → title `Rounds one and two` → short body → **Publish release**.
- Or with `gh`:
  `gh release create v1.0.0 --title "Rounds one and two" --notes "Cross-Engine Citation Study, rounds one and two: twelve B2B SaaS buyer questions, four AI engines, 19 June and 6 to 7 August 2026."`

The release must come **after** step 4. Zenodo does not backfill releases created
while the repository was switched off.

## 6. Check the record Zenodo produces **[LOGIN]**

Wait for the release to be processed, then open the record from the GitHub
integration page and check it against `.zenodo.json`:

- [ ] **Title** reads *Cross-Engine Citation Study, rounds one and two: sources and brands cited by ChatGPT, Perplexity, Gemini and Google's AI Overview*, not `minelgunesoglu-code/cross-engine-citation-study v1.0.0`, which
      is the fallback when `.zenodo.json` was not read.
- [ ] **Resource type** is *Dataset*.
- [ ] **Creator** is `Gunesoglu, Minel`, affiliation `Is My Brand in AI`, ORCID
      0009-0009-4823-6016, and it is the only one.
- [ ] **Licence** is *Creative Commons Attribution 4.0 International*.
- [ ] **Publication date** and **version** are what step 0 settled.
- [ ] **Description** renders as paragraphs, with no raw `<p>` tags.
- [ ] **Related identifiers** carry the article URL (*is supplement to*) and the
      GitHub repository.
- [ ] **Files**: one zip of the repository at the tag. `__pycache__/` is
      gitignored and correctly absent.
- [ ] Two DOIs exist: a **version DOI** for v1.0.0 and a **concept DOI** that
      always resolves to the newest version. Write both down.

Metadata can be edited on the record later; files in a published record cannot.

---

## 7. Add the DOI everywhere a reader will look **[LOCAL]**

Use the **concept DOI** in badges and citations, so they keep resolving to the
newest version.

1. **`README.md`**: replace the Archive row's text
   `DOI: to be added after the Zenodo release` with
   ```markdown
   [![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.XXXXXXXX.svg)](https://doi.org/10.5281/zenodo.XXXXXXXX) concept DOI, resolves to the latest version
   ```
   and add `https://doi.org/10.5281/zenodo.XXXXXXXX` to the suggested citation.
2. **`CITATION.cff`**: add, at the top level,
   ```yaml
   doi: "10.5281/zenodo.XXXXXXXX"
   identifiers:
     - type: doi
       value: "10.5281/zenodo.XXXXXXXX"
       description: Concept DOI, resolves to the latest version
     - type: doi
       value: "10.5281/zenodo.YYYYYYYY"
       description: Version 1.0.0
   ```
3. Commit and push. These edits do **not** need a new release.

```bash
git add README.md CITATION.cff
git commit -m "Add the Zenodo DOI to the README and citation metadata"
git push
```

## 8. Add the DOI to the site **[LOCAL, site repository]**

In the site repository:

- `content/do-ai-engines-cite-the-same-sources.md`, section **Cite this study** (the list of raw files): add the DOI link and the GitHub repository link.
- `app/research/page.tsx`: add the DOI to this study's `artifacts` line, as the
  other deposited studies do, and a "Repository" entry to its `data` list.
- If the page's dataset schema supports an identifier, add the DOI there.

Then deploy the site as usual.

---

## For a later version

Do not create a second, unrelated Zenodo record. Commit the new material, bump
`version` and `publication_date` in `.zenodo.json`, tag, and cut a new GitHub
Release on the same repository. Zenodo files it as a new version under the
**same concept DOI**.

---

## Which steps a machine cannot do

| Step | Why |
|---|---|
| 1. Create the GitHub repository | Authenticated write to GitHub |
| 3. Connect GitHub to Zenodo | OAuth consent on two logged-in accounts |
| 4. Toggle this repository on | Authenticated write; installs a webhook |
| 5. Publish the GitHub Release | Authenticated write to GitHub |
| 6. Inspect and edit the record | Zenodo session required; the DOI is permanent once minted |

Steps 2, 7, 8 and the tag command in 5 are ordinary local git work.
