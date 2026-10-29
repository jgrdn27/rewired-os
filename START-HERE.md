# Start with Rewired OS

**Change your AI. Keep your system.** A personal OS for your life, learning, projects, and work. Your model supplies intelligence; these files keep the context and continuity.

Download the [Rewired OS ZIP](https://github.com/jgrdn27/rewired-os/releases/download/v0.6.0-beta.3/rewired-os-0.6.0-beta.3.zip) and unzip it once into a new folder in Google Drive, OneDrive, Box, or your preferred shared storage. Keep the complete folder together and let it sync. Each assistant should use this same personal OS folder.

Give your assistant access to the folder and ask: **“Read START-HERE.md in my shared Rewired-OS folder and help me get started.”** Once the host loads its guidance, **“Let's get started”** or **“Let's go”** is enough. You do not need a website or a business to begin.

If you are reading this on GitHub, follow [INSTALL.md](INSTALL.md) to create your shared folder before personalization. If you already have a Rewired OS, connect to it and keep its existing context. For a requested update, use [UPDATE.md](UPDATE.md). Access to the repository or an uploaded snapshot is not access to your personal OS.

For the assistant:

1. Read [AGENTS.md](AGENTS.md), the small [preferences file](preferences.json), and [context index](context/index.md). Follow linked profile/setup records selectively to distinguish a new install from an existing or paused setup.
2. Establish that this is the user's intended shared OS folder, then check actual read/write capability. Reuse a known location rather than creating a fresh copy for this assistant. If only a repository, temporary checkout, or chat attachment is available, identify that access limit and help the user connect the existing folder or choose shared storage for a first install. Do not move files or connect an account without the user's request. Use [portability](docs/portability.md) when needed; provider names do not prove access or synchronization.
3. For a new or unfinished setup and an ordinary greeting such as “Let's go,” follow [Get started](workflows/first-win.md). Personalize first, one focused question at a time, with suggested answers and the option to skip. Offer website research when relevant; the OS also supports personal-only use. No automatic fictional call or GTM activation.
4. In an established OS, continue the user's work. If a greeting has no clear next task, offer a short choice to resume work, start something, or refresh setup. A specific task should not be delayed by onboarding. Use the [workflow index](workflows/index.md), reading visible workflows explicitly if native discovery is unavailable.
5. Preserve confirmed context and a resume point when authorized. If you cannot write, show what is unsaved and provide a handoff. Do not claim persistent setup from a chat-only summary.

The [GTM Library](library/README.md) is optional. It stays unloaded until the user activates it or explicitly asks for its help. Opening this folder does not authorize installation, account changes, credit use, or outreach.
