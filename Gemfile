source "https://rubygems.org"
# Hello! This is where you manage which Jekyll version is used to run.
# When you want to use a different version, change it below, save the
# file and run `bundle install`. Run Jekyll with `bundle exec`, like so:
#
#     bundle exec jekyll serve
#
# This will help ensure the proper Jekyll version is running.
# Happy Jekylling!
#gem "jekyll", ">= 3.9", "< 4.0"  # Lock Jekyll to GitHub Pages-supported version

gem "jekyll", "~> 4.3"

# Use the json that ships with Ruby rather than letting bundler fetch and
# compile a newer one. On Windows, a freshly built native extension is refused
# by Application Control ("An Application Control policy has blocked this
# file" on json/ext/generator.so), which stops jekyll from loading at all.
# 2.9.1 is Ruby 3.4's default gem and satisfies jekyll's json (~> 2.6).
gem "json", "2.9.1"  # Lock Jekyll to GitHub Pages-supported version

# This is the default theme for new Jekyll sites. You may change this to anything you like.
#gem "minima", "~> 2.5"
# If you want to use GitHub Pages, remove the "gem "jekyll"" above and
# uncomment the line below. To upgrade, run `bundle update github-pages`.
# gem "github-pages", group: :jekyll_plugins
# If you have any plugins, put them here!

group :jekyll_plugins do
  # jekyll-feed removed: the site has no _posts, so the feed it generated was
  # empty apart from a build timestamp - which was also the only file that
  # changed between two builds of identical content, defeating the SHA-256 in
  # the handover statement.
  gem "just-the-docs"
  gem "jekyll-spaceship"
  gem "jekyll-default-layout"
end


# Windows and JRuby do not include zoneinfo files, so bundle the tzinfo-data gem
# and associated library.
platforms :windows, :jruby do
  gem "tzinfo", "~> 2.0"
  gem "tzinfo-data"
end

# Performance-booster for watching directories on Windows
gem "wdm", "~> 0.2", platforms: [:windows]

# Required for Ruby 3.0+ (no longer bundled by default)
gem "webrick"

