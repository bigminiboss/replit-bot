q = {
    "markAsRead": "mutation MarkAllNotificationsAsSeen {markAllNotificationsAsSeen {id}}",
    "markOneAsRead": "mutation MarkAsSeen($id: Int) {markNotificationsAsSeen(id: $id)}",
    "replTitle": "query ReplTitle($title: String, $teamId: Int) {replTitle(title: $title, teamId: $teamId)}",
    "dashboardMoveItems": "mutation ReplsDashboardMoveItemsToFolder($replIds: [String!]!, $folderIds: [String!]!, $destFolderId: String!, $teamId: Int) {moveItemsToFolder(replIds: $replIds, folderIds: $folderIds, destFolderId: $destFolderId, teamId: $teamId) {... on Repl {id, ...ReplsDashboardReplItemRepl}, ... on ReplFolder {id, ...ReplsDashboardFolderItemReplFolder}}}, fragment ReplsDashboardReplItemRepl on Repl {id, ...ReplsDashboardReplItemActionsRepl, ...ReplLinkRepl, user {...UserLinkUser}}, fragment ReplsDashboardReplItemActionsRepl on Repl {id}, fragment ReplLinkRepl on Repl {id}, fragment UserLinkUser on User {id}, fragment ReplsDashboardFolderItemReplFolder on ReplFolder {id}",
    "dashboardItems": "query ReplsDashboardReplFolderList($path: String!, $starred: Boolean, $after: String) {currentUser {replFolderByPath(path: $path) {id, canEdit, canCreateSubFolders, parent {id}, folders {name, canEdit, timeCreated}, repls(starred: $starred, after: $after) {items {id, user {username}, config {isServer}}, pageInfo {nextCursor}}}}}",
    "updatePresence": "mutation {updateUserSitePresence {...on CurrentUser {id}}}",
    "replComments": "query Repl($id: String!, $after: String, $count: Int) {repl(id: $id) {... on Repl {comments(after: $after, count: $count) {items {\n\t\t\tid\n\t\t\ttimeCreated\n\t \t\ttimeUpdated\n\t\t\tbody\n\t\t\tbodyNoMarkdown: body(removeMarkdown: true)\n\t\t\tuser {\n\t \t\t\tusername\n\t\t\t}\n\t \t\tisHidden\n\t\t\trepl {\n\t\t\t\tid\n\t\t\t}\n\t \t\tparentComment {\n\t\t\t\tid\n\t\t\t}\n\t \t\tpost {\n\t\t\t\tid\n\t\t\t}\n\t\t\tcurrentUserPermissions {\n\t \t\t\tedit\n\t\t \t\tdelete\n\t\t \t\tbanAuthor\n\t\t \t\tcanHideComment\n\t\t \t\treport\n\t\t\t}\n\t\t}}}}}",
    "currentUser": """query {currentUser {
			id
			email
			username
			firstName
			lastName
			locale
			emailNotifications
			isVerified
			displayName
			fullName
			url
			bio
			socials {
				id
		 		url
				type
			}
			hasRepl
			hasPrivacyRole
			roles {
				id
		 		key
				name
		 		tagline
			}
			isLoggedIn
			isSubscribed
			timeCreated
			warnings {
				id
		 		reason
				moderator {
		 			username
				}
		 		timeCreated
			}
			followerCount
			followCount
			isBannedFromBoards
			isHacker
			cannySSOToken
			canUpdateEmail: canUpdate(column: EMAIL)
			canUpdateUsername: canUpdate(column: USERNAME)
			state {
				id
		 		skillLevel
				interestedIn
		 		languagesInterestedIn {
					id
					displayName
					icon
					tagline
				}
			}
			sidebarClosed
			hasProfileImage
			image
			coverImage {
				url
		 		offsetY
			}
			socialSignup
			googleAuth: auth(provider: GOOGLE) {
				accessToken
			}
			githubAuth: auth(provider: GITHUB) {
				accessToken
			}
			facebookAuth: auth(provider: FACEBOOK) {
				accessToken
			}
			gitHubInfo {
		 		installations {
					id
					type
					avatarUrl
					name
				}
		 		userInfo {
					name
					email
					avatarUrl
				}
			}
			usernameRepl {
				id
		 		title
				url
			}
			daysSinceSignup
			clui
			editorPreferences {
				isLayoutStacked
		 		theme
				fontSize
		 		indentIsSpaces
				indentSize
		 		keyboardHandler
				wrapping
				accessibleTerminal
		 		extraDelight
			}
		}}""",
    "currentUserPrevious": """query {currentUser {
			id
			email
			username
			firstName
			lastName
			locale
			emailNotifications
			isVerified
			displayName
			fullName
			url
			bio
			socials {
				id
		 		url
				type
			}
			hasRepl
			hasPrivacyRole
			roles {
				id
		 		key
				name
		 		tagline
			}
			isLoggedIn
			isSubscribed
			timeCreated
			warnings {
				id
		 		reason
				moderator {
		 			username
				}
		 		timeCreated
			}
			followerCount
			followCount
			isBannedFromBoards
			isHacker
			cannySSOToken
			canUpdateEmail: canUpdate(column: EMAIL)
			canUpdateUsername: canUpdate(column: USERNAME)
			state {
				id
		 		skillLevel
				interestedIn
		 		languagesInterestedIn {
					id
					displayName
					icon
					tagline
				}
			}
			device {
				isMobile
		 		isMac
			}
			sidebarClosed
			hasProfileImage
			image
			coverImage {
				url
		 		offsetY
			}
			socialSignup
			googleAuth: auth(provider: GOOGLE) {
				accessToken
			}
			githubAuth: auth(provider: GITHUB) {
				accessToken
			}
			facebookAuth: auth(provider: FACEBOOK) {
				accessToken
			}
			gitHubInfo {
		 		installations {
					id
					type
					avatarUrl
					name
				}
		 		userInfo {
					name
					email
					avatarUrl
				}
			}
			usernameRepl {
				id
		 		title
				url
			}
			daysSinceSignup
			clui
			editorPreferences {
				isLayoutStacked
		 		theme
				fontSize
		 		indentIsSpaces
				indentSize
		 		keyboardHandler
				wrapping
				accessibleTerminal
		 		extraDelight
			}
		}}""",
    "comment": "query Comment($id: Int!) {comment(id: $id) {id, body, voteCount, timeCreated, timeUpdated, user {username}, url, post {id}, parentComment {id}, isAuthor, canEdit, canVote, canComment, hasVoted, canReport, hasReported, isAnswer, canSelectAsAnswer, canUnselectAsAnswer}}",
    "restore": "mutation Mutation($title: String!) {clui {trash {restore(title: $title) {...CluiOutput}}}}, fragment CluiOutput on CluiOutput {... on CluiSuccessOutput {message, json}, ... on CluiErrorOutput {error, json}, ... on CluiMarkdownOutput {markdown}, ... on CluiComponentOutput {component}, ... on CluiTableOutput {columns {label, key}, rows}}",
    "dashboardDeleteFolder": "mutation ReplsDashboardFolderItemDelete($folderId: String!) {deleteReplFolder(folderId: $folderId) {id}}",
    "updateUser": "mutation UpdateCurrentUser($input: UpdateCurrentUserInput!) {updateCurrentUser(input: $input) {\n\t\t\tfirstName\n\t \t\tlastName\n\t\t\tbio\n\t\t\temailNotifications\n\t \t\timage\n\t\t}}",
    "deleteRepl": "mutation DeleteRepl($id: String!) {deleteRepl(id: $id) {id}}",
    "replComment": "query ReplComment($id: Int!) {replComment(id: $id) {...on ReplComment {\n\t\t\tid\n\t\t\tbody\n\t\t\ttimeCreated\n\t \t\ttimeUpdated\n\t\t\tuser {\n\t \t\t\tusername\n\t\t\t}\n\t \t\tisHidden\n\t\t\tpost {\n\t \t\t\tid\n\t\t\t}\n\t \t\trepl {\n\t\t\t\tid\n\t\t\t}\n\t \t\tparentComment {\n\t\t\t\tid\n\t\t \t\tbody\n\t\t\t\ttimeCreated\n\t\t \t\ttimeUpdated\n\t\t\t\tuser {\n\t\t \t\t\tusername\n\t\t\t\t}\n\t\t\t\tpost {\n\t\t \t\t\tid\n\t\t\t\t}\n\t\t \t\trepl {\n\t\t\t\t\tid\n\t\t\t\t}\n\t\t \t\tcomments: replies {\n\t\t\t\t\tid\n\t\t\t\t}\n\t\t \t\tcanComment\n\t\t\t}\n\t \t\tcomments: replies {\n\t\t\t\tid\n\t\t \t\tbody\n\t\t\t\ttimeCreated\n\t\t \t\ttimeUpdated\n\t\t\t\tuser {\n\t\t \t\t\tusername\n\t\t\t\t}\n\t\t \t\trepl {\n\t\t\t\t\tid\n\t\t\t\t}\n\t\t \t\tparentComment {\n\t\t\t\t\tid\n\t\t\t\t}\n\t\t \t\tcanComment\n\t\t\t}\n\t \t\tcanComment\n\t\t} ...on UserError {message}}}",
    "user": "query User($id: Int!) {user(id: $id) {\n\t \t\tid\n\t\t\tusername\n\t\t\tfirstName\n\t\t\tlastName\n\t\t\tlocale\n\t\t\tisVerified\n\t\t\tdisplayName\n\t\t\tfullName\n\t\t\turl\n\t\t\tbio\n\t\t\tsocials {\n\t\t\t\tid\n\t\t \t\turl\n\t\t\t\ttype\n\t\t\t}\n\t\t\troles {\n\t\t\t\tid\n\t\t \t\tkey\n\t\t\t\tname\n\t\t \t\ttagline\n\t\t\t}\n\t\t\tisFollowedByCurrentUser\n\t\t\tisFollowingCurrentUser\n\t\t\tisBlockedByCurrentUser\n\t\t\tisBlockingCurrentUser\n\t\t\tisLoggedIn\n\t\t\tisSubscribed\n\t\t\ttimeCreated\n\t\t\tfollowerCount\n\t\t\tfollowCount\n\t\t\tisHacker\n\t\t\timage\n\t\t\tcoverImage {\n\t\t\t\turl\n\t\t \t\toffsetY\n\t\t\t}\n\t\t\tpresenceStatus {\n\t\t\t\tlastSeen\n\t\t \t\tisOnline\n\t\t\t}\n\t\t}}",
    "createReplComment": "mutation CreateReplComment($input: CreateReplCommentInput!) {createReplComment(input: $input) {...on UserError {message} ...on ReplComment {\n\t\t\tid\n\t \t\tbody\n\t\t\ttimeCreated\n\t \t\ttimeUpdated\n\t\t\tuser {\n\t \t\t\tusername\n\t\t\t}\n\t\t\tpost {\n\t \t\t\tid\n\t\t\t}\n\t \t\trepl {\n\t\t\t\tid\n\t\t\t}\n\t \t\tcanEdit\n\t\t}}}",
    "trash": "query Query {clui {trash {view {...CluiOutput}}}}, fragment CluiOutput on CluiOutput {... on CluiSuccessOutput {message, json}, ... on CluiErrorOutput {error, json}, ... on CluiMarkdownOutput {markdown}, ... on CluiComponentOutput {component}, ... on CluiTableOutput {columns {label, key}, rows}}",
    "removeMultiplayer": "mutation RemoveMultiplayerUser($username: String!, $replId: String!) {removeMultiplayerUser(username: $username, replId: $replId) {id}}",
    "following": "query FollowModalFollows($username: String!, $after: String, $count: Int) {currentUser {id}, user: userByUsername(username: $username) {id, follows(after: $after, count: $count) {items {id, ...FollowModalUser}, pageInfo {hasNextPagenextCursor}}}}, fragment FollowModalUser on User {...UserLinkUser, id, username, fullName, image, isFollowedByCurrentUser, followerCount}, fragment UserLinkUser on User {id, url, username}",
    "userByUsername": "query UserByUsername($username: String!) {userByUsername(username: $username) {\n\t \t\tid\n\t\t\tusername\n\t\t\tfirstName\n\t\t\tlastName\n\t\t\tlocale\n\t\t\tisVerified\n\t\t\tdisplayName\n\t\t\tfullName\n\t\t\turl\n\t\t\tbio\n\t\t\tsocials {\n\t\t\t\tid\n\t\t \t\turl\n\t\t\t\ttype\n\t\t\t}\n\t\t\troles {\n\t\t\t\tid\n\t\t \t\tkey\n\t\t\t\tname\n\t\t \t\ttagline\n\t\t\t}\n\t\t\tisFollowedByCurrentUser\n\t\t\tisFollowingCurrentUser\n\t\t\tisBlockedByCurrentUser\n\t\t\tisBlockingCurrentUser\n\t\t\tisLoggedIn\n\t\t\tisSubscribed\n\t\t\ttimeCreated\n\t\t\tfollowerCount\n\t\t\tfollowCount\n\t\t\tisHacker\n\t\t\timage\n\t\t\tcoverImage {\n\t\t\t\turl\n\t\t \t\toffsetY\n\t\t\t}\n\t\t\tpresenceStatus {\n\t\t\t\tlastSeen\n\t\t \t\tisOnline\n\t\t\t}\n\t\t}}",
    "userPosts": "query ProfilePosts($username: String!, $after: String, $order: String, $count: Int) {userByUsername(username: $username) {posts(after: $after, order: $order, count: $count) {items {\n\t\t\tid\n\t \t\ttitle\n\t\t\tshowHosted\n\t \t\tcommentCount\n\t\t\tisPinned\n\t \t\tisHidden\n\t\t\tisLocked\n\t \t\ttimeCreated\n\t\t\ttimeUpdated\n\t \t\tbody\n\t\t\turl\n\t \t\tuser {\n\t\t\t\tusername\n\t\t\t}\n\t \t\tboard {\n\t\t\t\tid\n\t\t\t}\n\t \t\trepl {\n\t\t\t\tid\n\t\t\t}\n\t \t\treplComment {\n\t\t\t\tid\n\t\t\t}\n\t\t}}}}",
    "post": "query Post($id: Int!) {post(id: $id) {\n\t\t\tid\n\t \t\ttitle\n\t\t\tshowHosted\n\t \t\tcommentCount\n\t\t\tisPinned\n\t \t\tisHidden\n\t\t\tisLocked\n\t \t\ttimeCreated\n\t\t\ttimeUpdated\n\t \t\tbody\n\t \t\tuser {\n\t\t\t\tusername\n\t\t\t}\n\t \t\trepl {\n\t\t\t\tid\n\t\t\t}\n\t \t\treplComment {\n\t\t\t\tid\n\t\t\t\tbody\n\t\t\t\ttimeCreated\n\t\t \t\ttimeUpdated\n\t\t\t\tuser {\n\t\t \t\t\tusername\n\t\t\t\t}\n\t\t \t\tisHidden\n\t\t \t\trepl {\n\t\t\t\t\tid\n\t\t\t\t}\n\t\t \t\tparentComment {\n\t\t\t\t\tid\n\t\t\t \t\tbody\n\t\t\t\t\ttimeCreated\n\t\t\t \t\ttimeUpdated\n\t\t\t\t\tuser {\n\t\t\t \t\t\tusername\n\t\t\t\t\t}\n\t\t\t\t\tpost {\n\t\t\t \t\t\tid\n\t\t\t\t\t}\n\t\t\t \t\trepl {\n\t\t\t\t\t\tid\n\t\t\t\t\t}\n\t\t\t \t\tcomments: replies {\n\t\t\t\t\t\tid\n\t\t\t\t\t}\n\t\t\t \t\tcanComment\n\t\t\t\t}\n\t\t \t\tcomments: replies {\n\t\t\t\t\tid\n\t\t\t \t\tbody\n\t\t\t\t\ttimeCreated\n\t\t\t \t\ttimeUpdated\n\t\t\t\t\tuser {\n\t\t\t \t\t\tusername\n\t\t\t\t\t}\n\t\t\t \t\trepl {\n\t\t\t\t\t\tid\n\t\t\t\t\t}\n\t\t\t \t\tparentComment {\n\t\t\t\t\t\tid\n\t\t\t\t\t}\n\t\t\t \t\tcanComment\n\t\t\t\t}\n\t\t \t\tcanComment\n\t\t\t}\n\t\t}}",
    "createRepl": "mutation CreateRepl($input: CreateReplInput!) {createRepl(input: $input) {... on Repl {\n\t\t\tid\n\t\t \tisProject\n\t\t \tisPrivate\n\t\t \tisStarred\n\t\t \ttitle\n\t\t \tslug\n\t\t \timageUrl\n\t\t \tfolderId\n\t\t \tisRenamed\n\t\t \tcommentCount\n\t\t \tlikeCount\n\t\t \tcurrentUserDidLike\n\t\t \ttemplateCategory\n\t\t \twasPosted\n\t\t \twasPublished\n\t\t \tlayoutState\n\t\t \tlanguage\n\t\t \towner: user {\n\t\t \t\tid\n\t\t\t\tusername\n\t\t\t\tfirstName\n\t\t\t\tlastName\n\t\t\t\tlocale\n\t\t\t\tisVerified\n\t\t\t\tdisplayName\n\t\t\t\tfullName\n\t\t\t\turl\n\t\t\t\tbio\n\t\t\t\tsocials {\n\t\t\t\t\tid\n\t\t\t \t\turl\n\t\t\t\t\ttype\n\t\t\t\t}\n\t\t\t\troles {\n\t\t\t\t\tid\n\t\t\t \t\tkey\n\t\t\t\t\tname\n\t\t\t \t\ttagline\n\t\t\t\t}\n\t\t\t\tisFollowedByCurrentUser\n\t\t\t\tisFollowingCurrentUser\n\t\t\t\tisBlockedByCurrentUser\n\t\t\t\tisBlockingCurrentUser\n\t\t\t\tisLoggedIn\n\t\t\t\tisSubscribed\n\t\t\t\ttimeCreated\n\t\t\t\tfollowerCount\n\t\t\t\tfollowCount\n\t\t\t\tisHacker\n\t\t\t\timage\n\t\t\t\tcoverImage {\n\t\t\t\t\turl\n\t\t\t \t\toffsetY\n\t\t\t\t}\n\t\t\t\tpresenceStatus {\n\t\t\t\t\tlastSeen\n\t\t\t \t\tisOnline\n\t\t\t\t}\n\t\t\t}\n\t\t\torigin {\n\t\t\t\tid\n\t\t \t\ttitle\n\t\t\t}\n\t\t\tlang {\n\t\t\t\tid\n\t\t \t\tdisplayName\n\t\t \t\tcanUseShellRunner\n\t\t\t}\n\t\t\ticonUrl\n\t\t\ttemplateLabel\n\t\t\turl\n\t\t\tinviteUrl\n\t\t\tmultiplayerInvites {\n\t\t\t\temail\n\t\t \t\treplId\n\t\t\t\ttype\n\t\t\t}\n\t\t\thistoryUrl\n\t\t\tanalyticsUrl\n\t\t\trootOriginReplUrl\n\t\t\ttimeCreated\n\t\t\ttimeUpdated\n\t\t\tisOwner\n\t\t\tconfig {\n\t\t\t\tisServer\n\t\t \t\tgitRemoteUrl\n\t\t\t\tdomain\n\t\t \t\tisVnc\n\t\t \t\tdoClone\n\t\t\t}\n\t\t\tpinnedToProfile\n\t\t\tsize\n\t\t\thostedUrl\n\t\t\thostedUrlDotty: hostedUrl(dotty: true)\n\t\t\thostedUrlDev: hostedUrl(dev: true)\n\t\t\thostedUrlNoCustom: hostedUrl(noCustomDomain: true)\n\t\t\tterminalUrl\n\t\t\tcurrentUserPermissions {\n\t\t\t\tchangeTitle\n\t\t \t\tchangeDescription\n\t\t\t\tchangeImageUrl\n\t\t \t\tchangeIconUrl\n\t\t\t\tchangeTemplateLabel\n\t\t \t\tchangeLanguage\n\t\t\t\tchangeConfig\n\t\t \t\tchangePrivacy\n\t\t\t\tstar\n\t\t \t\tpin\n\t\t\t\tmove\n\t\t \t\tdelete\n\t\t\t\tleaveMultiplayer\n\t\t \t\teditMultiplayers\n\t\t\t\tviewHistory\t\n\t\t \t\tcontainerAttach\n\t\t\t\tcontainerWrite\n\t\t \t\tchangeAlwaysOn\n\t\t\t\tlinkDomain\n\t\t \t\twriteTests\n\t\t\t\tchangeCommentSettings\n\t\t \t\tinviteGuests\n\t\t\t\tpublish\n\t\t \t\tfork\n\t\t\t}\n\t\t\tdatabase {\n\t\t\t\tid\n\t\t \t\tkeysCount\n\t\t\t\tsizeMB\n\t\t\t\tjwt\n\t\t\t}\n\t\t\ttemplate {\n\t\t\t\tid\n\t\t\t}\n\t\t\tisProjectFork\n\t\t\tisModelSolution\n\t\t\tisModelSolutionFork\n\t\t\tworkspaceCta\n\t\t\tsubmission {\n\t\t\t\tid\n\t\t \t\ttimeSubmitted\n\t\t\t\ttimeLastReviewed\n\t\t \t\tisGroupSubmission\n\t\t\t\tauthor {\n\t\t \t\t\tusername\n\t\t\t\t}\n\t\t \t\tsubmissionGroup {\n\t\t\t\t\tusers {\n\t\t\t\t\t\tusername\n\t\t\t\t\t}\n\t\t\t\t}\n\t\t\t}\n\t\t\tcommentSettings {\n\t\t\t\tid\n\t\t \t\tenabled\n\t\t\t}\n\t\t\tpublicForkCount\n\t\t\trunCount\n\t\t\tisAlwaysOn\n\t\t\tisBoosted\n\t\t\ttags {\n\t\t\t\tid\n\t\t \t\tisOfficial\n\t\t\t}\n\t\t\tlastPublishedAt\n\t\t\tmultiplayers {\n\t\t\t\tusername\n\t\t\t}\n\t\t\tnixedLanguage\n\t\t\tpublishedAs\n\t\t\tattachments {\n\t\t\t\tid\n\t\t \t\tfileName\n\t\t\t\tmimeType\n\t\t \t\ttimeCreated\n\t\t\t\ttimeUpdated\n\t\t \t\tcontents\n\t\t\t}\n\t\t\tdescription(plainText: true)\n\t\t\tmarkdownDescription: description(plainText: false)\n\t\t\thasExplainCode\n\t\t\thasGenerateCode\n\t\t\ttemplateInfo {\n\t\t\t\tlabel\n\t\t \t\ticonUrl\n\t\t\t}\n\t\t\tdomains {\n\t\t\t\tdomain\n\t\t \t\tstate\n\t\t\t}\n\t\t\tapexProxy\n\t\t\treplViewSettings {\n\t\t\t\tid\n\t\t \t\tdefaultView\n\t\t\t\treplFile\n\t\t \t\treplImage\n\t\t\t}\n\t\t\tpowerUpCosts {\n\t\t\t\t...on UnauthorizedError {\n\t\t \t\t\tmessage\n\t\t\t\t}\n\t\t \t\t...on NotFoundError {\n\t\t\t\t\tmessage\n\t\t\t\t}\n\t\t \t\t...on PowerUpCostsType {\n\t\t\t\t\tboost {\n\t\t\t\t\t\tcycles\n\t\t\t \t\t\texplanation\n\t\t\t\t\t}\n\t\t\t\t\talwaysOn {\n\t\t\t\t\t\tcycles\n\t\t\t \t\t\texplanation\n\t\t\t\t\t}\n\t\t\t\t}\n\t\t\t}\n\t\t\tisTutorial\n\t\t}}}",
    "postComments": "mutation createReplComment($input: CreateReplCommentInput!) { createReplComment(input: $input) { ...on ReplComment { $input } } }",
    "getUserEventsFeed": "query getUserEventsFeed($count: Int!, $after: String!) {\n        getUserEventsFeed(count: $count, after: $after) {\n          ... on UserEventConnection {\n            items {\n              id\n              user { username }\n              following { username }\n              comment { body repl { url } }\n              reaction { reactionType }\n              repl { title url }\n              eventType\n            }\n          }\n        }\n      }",
    "changeUsername": "mutation Mutation($username: String!) {clui {account {changeUsername(username: $username) {...CluiOutput}}}}, fragment CluiOutput on CluiOutput {... on CluiSuccessOutput {message, json}, ... on CluiErrorOutput {error, json}, ... on CluiMarkdownOutput {markdown}, ... on CluiComponentOutput {component}, ... on CluiTableOutput {columns {label, key}, rows}}",
    "ReplNews": "query ReplNews($count: Int!, $options: ReplPostsQueryOptions!, $username: String!) {\n      pinnedPosts { title repl { url } user { username } }\n      siteBanner { id message }\n      trendingReplPosts(count: $count) { repl { id title url description user { username } } }\n      replPosts(options: $options) { items { repl { title url description user { username } } } }\n      userByUsername(username: $username) { presenceStatus { lastSeen isOnline } }\n    }",
    "replThreads": "query Repl($id: String) {repl(id: $id) {...on Repl {\n\t\t\tannotationAnchors {\n\t\t\t\tid\n\t\t \t\tpath\n\t\t\t\totVersion\n\t\t \t\tindexStart\n\t\t\t\tindexEnd\n\t\t \t\ttimeCreated\n\t\t\t\ttimeUpdated\n\t\t \t\tisResolved\n\t\t\t\tmessages {\n\t\t \t\t\tid\n\t\t\t \t\ttimeCreated\n\t\t\t \t\ttimeUpdated\n\t\t\t \t\tcontent {\n\t\t\t \t\t\t...on TextMessageContentType {\n\t\t\t\t\t\t\ttext\n\t\t\t\t\t\t}\n\t\t\t \t\t\t...on StatusMessageContentType {\n\t\t\t\t\t\t\tstatus\n\t\t\t\t\t\t}\n\t\t\t \t\t\t...on PreviewMessageContentType {\n\t\t\t\t\t\t\tpreview\n\t\t\t\t\t\t}\n\t\t\t\t\t}\n\t\t\t \t\tuser {\n\t\t\t \t\t\tusername\n\t\t\t\t\t}\n\t\t\t\t\tseen\n\t\t\t\t\tcurrentUserIsAuthor\n\t\t\t\t}\n\t\t \t\tparticipants {\n\t\t\t\t\tusername\n\t\t\t\t}\n\t\t \t\tmessageCount\n\t\t\t\tunreadCount\n\t\t \t\tcurrentUserIsAuthor\n\t\t\t\tisGeneral\n\t\t\t}\n\t\t}}}",
    "clientUser": "query {currentUser {id, username, firstName, lastName, bio, isVerified, displayName, fullName, url, roles {id, name, tagline}, isLoggedIn, timeCreated, isHacker, languages {id}, image, email, state {id, skillLevel, interestedIn}, device {isMobile, isMac}, notificationCount}}",
    "userRepls": "query UserByUsername($username: String!, $count: Int = 50) {userByUsername(username: $username){publicRepls(showUnnamed: true, count: $count){items{id, title, slug, description, isRenamed, user {username}, lang {id}, url, timeCreated, timeUpdated, hostedUrl}}}}",
    "repl": "query Repl($id: String, $url: String) {repl(id: $id, url: $url) {...on Repl {\n\t\t\tid\n\t\t \tisProject\n\t\t \tisPrivate\n\t\t \tisStarred\n\t\t \ttitle\n\t\t \tslug\n\t\t \timageUrl\n\t\t \tfolderId\n\t\t \tisRenamed\n\t\t \tcommentCount\n\t\t \tlikeCount\n\t\t \tcurrentUserDidLike\n\t\t \ttemplateCategory\n\t\t \twasPosted\n\t\t \twasPublished\n\t\t \tlayoutState\n\t\t \tlanguage\n\t\t \towner: user {\n\t\t \t\tid\n\t\t\t\tusername\n\t\t\t\tfirstName\n\t\t\t\tlastName\n\t\t\t\tlocale\n\t\t\t\tisVerified\n\t\t\t\tdisplayName\n\t\t\t\tfullName\n\t\t\t\turl\n\t\t\t\tbio\n\t\t\t\tsocials {\n\t\t\t\t\tid\n\t\t\t \t\turl\n\t\t\t\t\ttype\n\t\t\t\t}\n\t\t\t\troles {\n\t\t\t\t\tid\n\t\t\t \t\tkey\n\t\t\t\t\tname\n\t\t\t \t\ttagline\n\t\t\t\t}\n\t\t\t\tisFollowedByCurrentUser\n\t\t\t\tisFollowingCurrentUser\n\t\t\t\tisBlockedByCurrentUser\n\t\t\t\tisBlockingCurrentUser\n\t\t\t\tisLoggedIn\n\t\t\t\tisSubscribed\n\t\t\t\ttimeCreated\n\t\t\t\tfollowerCount\n\t\t\t\tfollowCount\n\t\t\t\tisHacker\n\t\t\t\timage\n\t\t\t\tcoverImage {\n\t\t\t\t\turl\n\t\t\t \t\toffsetY\n\t\t\t\t}\n\t\t\t\tpresenceStatus {\n\t\t\t\t\tlastSeen\n\t\t\t \t\tisOnline\n\t\t\t\t}\n\t\t\t}\n\t\t\torigin {\n\t\t\t\tid\n\t\t \t\ttitle\n\t\t\t}\n\t\t\tlang {\n\t\t\t\tid\n\t\t \t\tdisplayName\n\t\t \t\tcanUseShellRunner\n\t\t\t}\n\t\t\ticonUrl\n\t\t\ttemplateLabel\n\t\t\turl\n\t\t\tinviteUrl\n\t\t\tmultiplayerInvites {\n\t\t\t\temail\n\t\t \t\treplId\n\t\t\t\ttype\n\t\t\t}\n\t\t\tanalyticsUrl\n\t\t\trootOriginReplUrl\n\t\t\ttimeCreated\n\t\t\ttimeUpdated\n\t\t\tisOwner\n\t\t\tconfig {\n\t\t\t\tisServer\n\t\t \t\tgitRemoteUrl\n\t\t\t\tdomain\n\t\t \t\tisVnc\n\t\t \t\tdoClone\n\t\t\t}\n\t\t\tpinnedToProfile\n\t\t\tsize\n\t\t\thostedUrl\n\t\t\thostedUrlDotty: hostedUrl(dotty: true)\n\t\t\thostedUrlDev: hostedUrl(dev: true)\n\t\t\thostedUrlNoCustom: hostedUrl(noCustomDomain: true)\n\t\t\tterminalUrl\n\t\t\tcurrentUserPermissions {\n\t\t\t\tchangeTitle\n\t\t \t\tchangeDescription\n\t\t\t\tchangeImageUrl\n\t\t \t\tchangeIconUrl\n\t\t\t\tchangeTemplateLabel\n\t\t \t\tchangeLanguage\n\t\t\t\tchangeConfig\n\t\t \t\tchangePrivacy\n\t\t\t\tstar\n\t\t \t\tpin\n\t\t\t\tmove\n\t\t \t\tdelete\n\t\t\t\tleaveMultiplayer\n\t\t \t\teditMultiplayers\n\t\t\t\tviewHistory\t\n\t\t \t\tcontainerAttach\n\t\t\t\tcontainerWrite\n\t\t \t\tchangeAlwaysOn\n\t\t\t\tlinkDomain\n\t\t \t\twriteTests\n\t\t\t\tchangeCommentSettings\n\t\t \t\tinviteGuests\n\t\t\t\tpublish\n\t\t \t\tfork\n\t\t\t}\n\t\t\tdatabase {\n\t\t\t\tid\n\t\t \t\tkeysCount\n\t\t\t\tsizeMB\n\t\t\t\tjwt\n\t\t\t}\n\t\t\ttemplate {\n\t\t\t\tid\n\t\t\t}\n\t\t\tisProjectFork\n\t\t\tisModelSolution\n\t\t\tisModelSolutionFork\n\t\t\tworkspaceCta\n\t\t\tsubmission {\n\t\t\t\tid\n\t\t \t\ttimeSubmitted\n\t\t\t\ttimeLastReviewed\n\t\t \t\tisGroupSubmission\n\t\t\t\tauthor {\n\t\t \t\t\tusername\n\t\t\t\t}\n\t\t \t\tsubmissionGroup {\n\t\t\t\t\tusers {\n\t\t\t\t\t\tusername\n\t\t\t\t\t}\n\t\t\t\t}\n\t\t\t}\n\t\t\tcommentSettings {\n\t\t\t\tid\n\t\t \t\tenabled\n\t\t\t}\n\t\t\tpublicForkCount\n\t\t\trunCount\n\t\t\tisAlwaysOn\n\t\t\tisBoosted\n\t\t\ttags {\n\t\t\t\tid\n\t\t \t\tisOfficial\n\t\t\t}\n\t\t\tlastPublishedAt\n\t\t\tmultiplayers {\n\t\t\t\tusername\n\t\t\t}\n\t\t\tnixedLanguage\n\t\t\tpublishedAs\n\t\t\tattachments {\n\t\t\t\tid\n\t\t \t\tfileName\n\t\t\t\tmimeType\n\t\t \t\ttimeCreated\n\t\t\t\ttimeUpdated\n\t\t \t\tcontents\n\t\t\t}\n\t\t\tdescription(plainText: true)\n\t\t\tmarkdownDescription: description(plainText: false)\n\t\t\thasExplainCode\n\t\t\thasGenerateCode\n\t\t\ttemplateInfo {\n\t\t\t\tlabel\n\t\t \t\ticonUrl\n\t\t\t}\n\t\t\tdomains {\n\t\t\t\tdomain\n\t\t \t\tstate\n\t\t\t}\n\t\t\tapexProxy\n\t\t\treplViewSettings {\n\t\t\t\tid\n\t\t \t\tdefaultView\n\t\t\t\treplFile\n\t\t \t\treplImage\n\t\t\t}\n\t\t\tpowerUpCosts {\n\t\t\t\t...on UnauthorizedError {\n\t\t \t\t\tmessage\n\t\t\t\t}\n\t\t \t\t...on NotFoundError {\n\t\t\t\t\tmessage\n\t\t\t\t}\n\t\t \t\t...on PowerUpCostsType {\n\t\t\t\t\tboost {\n\t\t\t\t\t\tcycles\n\t\t\t \t\t\texplanation\n\t\t\t\t\t}\n\t\t\t\t\talwaysOn {\n\t\t\t\t\t\tcycles\n\t\t\t \t\t\texplanation\n\t\t\t\t\t}\n\t\t\t\t}\n\t\t\t}\n\t\t\tisTutorial\n\t\t}}}",
    "notifications": "query notifications($after: String, $count: Int, $seen: Boolean) {notifications(after: $after, count: $count, seen: $seen) {items {...NotificationItems}}}, fragment NotificationItems on Notification {... on BasicNotification {id, ...BasicNotificationItemNotification}, ... on MentionedInPostNotification {id, ...NotificationItemMentionedInPostNotification}, ... on RepliedToPostNotification {id, ...NotificationItemRepliedToPostNotification}, ... on MentionedInCommentNotification {id, ...NotificationItemMentionedInCommentNotification}, ... on RepliedToCommentNotification {id, ...NotificationItemRepliedToCommentNotification}, ... on AnswerAcceptedNotification {id, ...NotificationItemAnswerAcceptedNotification}, ... on MultiplayerInvitedNotification {id, ...NotificationItemMultiplayerInvitedNotification}, ... on MultiplayerJoinedEmailNotification {id, ...NotificationItemMultiplayerJoinedEmailNotification}, ... on MultiplayerJoinedLinkNotification {id, ...NotificationItemMultiplayerJoinedLinkNotification}, ... on MultiplayerOverlimitNotification {id, ...NotificationItemMultiplayerOverlimitNotification}, ... on WarningNotification {id, ...NotificationItemWarningNotification}, ... on AnnotationNotification {id, ...NotificationItemAnnotationNotification}, ... on ThreadNotification {id, ...NotificationItemThreadNotification}, ... on TeamInviteNotification {id, ...NotificationItemTeamInviteNotification}, ... on TeamOrganizationInviteNotification {id, ...NotificationItemTeamOrganizationInviteNotification}, ... on TeamTemplateSubmittedNotification {id, ...NotificationTeamTemplateSubmittedNotification}, ... on TeamTemplateReviewedStatusNotification {id, ...NotificationTeamTemplateReviewedStatusNotification}, ... on EditRequestCreatedNotification {id, __typename}, ... on EditRequestAcceptedNotification {id, __typename}, ... on ReplCommentCreatedNotification {id, ...NotificationReplCommentCreatedNotification}, ... on ReplCommentReplyCreatedNotification {id, ...NotificationReplCommentReplyCreatedNotification}, ... on ReplCommentMentionNotification {id, ...NotificationReplCommentMentionNotification}, ... on NewFollowerNotification {id, ...NotificationItemNewFollower}}, fragment BasicNotificationItemNotification on BasicNotification {id, text, url, timeCreated, seen, context, __typename}, fragment NotificationItemMentionedInPostNotification on MentionedInPostNotification {id, text, url, timeCreated, seen, creator {id, ...NotificationItemCreator}, post {id, ...NotificationItemPost, board {id, ...NotificationItemBoard}}, __typename}, fragment NotificationItemCreator on User {username, image, __typename}, fragment NotificationItemPost on Post {id, title, url, __typename}, fragment NotificationItemBoard on Board {id, name, url, color, slug, __typename}, fragment NotificationItemRepliedToPostNotification on RepliedToPostNotification {id, text, url, timeCreated, seen, creator {id, ...NotificationItemCreator}, comment {id, post {id, ...NotificationItemPost, board {id, ...NotificationItemBoard}}}, __typename}, fragment NotificationItemMentionedInCommentNotification on MentionedInCommentNotification {id, text, url, timeCreated, seen, creator {id, ...NotificationItemCreator}, comment {id, post {id, ...NotificationItemPost, board {id, ...NotificationItemBoard}}}, __typename}, fragment NotificationItemRepliedToCommentNotification on RepliedToCommentNotification {id, text, url, timeCreated, seen, creator {id, ...NotificationItemCreator}, comment {id, body, post {id, ...NotificationItemPost, board {id, ...NotificationItemBoard}}}, __typename}, fragment NotificationItemAnswerAcceptedNotification on AnswerAcceptedNotification {id, text, url, timeCreated, seen, creator {id, ...NotificationItemCreator}, post {id, ...NotificationItemPost, board {id, ...NotificationItemBoard}}, __typename}, fragment NotificationItemMultiplayerInvitedNotification on MultiplayerInvitedNotification {id, text, url, timeCreated, seen, creator {id, ...NotificationItemCreator}, __typename}, fragment NotificationItemMultiplayerJoinedEmailNotification on MultiplayerJoinedEmailNotification {id, text, url, timeCreated, seen, creator {id, ...NotificationItemCreator}, __typename}, fragment NotificationItemMultiplayerJoinedLinkNotification on MultiplayerJoinedLinkNotification {id, text, url, timeCreated, seen, creator {id, ...NotificationItemCreator}, __typename}, fragment NotificationItemMultiplayerOverlimitNotification on MultiplayerOverlimitNotification {id, text, url, timeCreated, seen, creator {id, ...NotificationItemCreator}, __typename}, fragment NotificationItemWarningNotification on WarningNotification {id, text, url, timeCreated, seen, __typename}, fragment NotificationItemAnnotationNotification on AnnotationNotification {id, text, url, timeCreated, seen, creator {id, ...NotificationItemCreator}, __typename}, fragment NotificationItemThreadNotification on ThreadNotification {id, text, url, timeCreated, seen, creator {id, ...NotificationItemCreator}, participants {id, ...NotificationItemCreator}, thread {id, repl {id, url, slug, nextPagePathname, user {id, username}}}, __typename}, fragment NotificationItemTeamInviteNotification on TeamInviteNotification {id, text, url, timeCreated, seen, invite {id, ...NotificationItemTeamInvite}, __typename}, fragment NotificationItemTeamInvite on TeamInvite {id, team {id, displayName, username}, __typename}, fragment NotificationItemTeamOrganizationInviteNotification on TeamOrganizationInviteNotification {id, text, url, timeCreated, seen, invite {id, ...NotificationItemTeamOrganizationInvite}, __typename}, fragment NotificationItemTeamOrganizationInvite on TeamOrganizationInvite {id, organization {id, name}, __typename}, fragment NotificationTeamTemplateSubmittedNotification on TeamTemplateSubmittedNotification {id, text, url, timeCreated, seen, repl {id, url}, __typename}, fragment NotificationTeamTemplateReviewedStatusNotification on TeamTemplateReviewedStatusNotification {id, text, url, timeCreated, seen, repl {id, url}, __typename}, fragment NotificationReplCommentCreatedNotification on ReplCommentCreatedNotification {id, url, timeCreated, seen, replComment {id, ...NotificationReplCommentNotificationReplComment}, creator {id, ...NotificationItemCreator}, __typename}, fragment NotificationReplCommentNotificationReplComment on ReplComment {id, repl {title, url}, body, __typename}, fragment NotificationReplCommentReplyCreatedNotification on ReplCommentReplyCreatedNotification {id, timeCreated, seen, creator {id, ...NotificationItemCreator}, replComment {id, ...NotificationReplCommentNotificationReplComment}, __typename}, fragment NotificationReplCommentMentionNotification on ReplCommentMentionNotification {id, timeCreated, seen, creator {id, ...NotificationItemCreator}, replComment {id, parentComment {id, body, user {username, image}}, ...NotificationReplCommentNotificationReplComment}, __typename}, fragment NotificationItemNewFollower on NewFollowerNotification {id, timeCreated, seen, creator {...NotificationItemCreator}, __typename}",
    "replId": "query Repl($id: String!) {repl(id: $id) {... on Repl {id, title, slug, description, lang {id}, url, timeCreated, timeUpdated, hostedUrl}}}",
    "updateRepl": "mutation ReplsDashboardUpdateRepl($input: UpdateReplInput!) {updateRepl(input: $input) {repl {\n\t\t\ttitle\n\t \t\tdescription\n\t\t\timageUrl\n\t \t\ticonUrl\n\t\t\tisPrivate\n\t \t\tisStarred\n\t\t\tlanguage\n\t \t\tslug\n\t\t}}",
    "viewTrash": "query Query {clui {trash {view {...CluiOutput}}}}, fragment CluiOutput on CluiOutput {... on CluiSuccessOutput {message, json}, ... on CluiErrorOutput {error, json}, ... on CluiMarkdownOutput {markdown}, ... on CluiComponentOutput {component}, ... on CluiTableOutput {columns {label, key}, rows}}",
    "sendReplCommentReply": "mutation CreateReplCommentReply($input: CreateReplCommentReplyInput!) {createReplCommentReply(input: $input) {...on UserError {message} ...on ReplComment {\n\t\t\tid\n\t \t\tbody\n\t\t\ttimeCreated\n\t \t\ttimeUpdated\n\t\t\tuser {\n\t \t\t\tusername\n\t\t\t}\n\t \t\trepl {\n\t\t\t\tid\n\t\t\t}\n\t \t\tcanEdit\n\t\t}}}",
    "leaderboard": "query {leaderboard {items {username}}}",
    "replNews": "query ReplNews($count: Int!, $options: ReplPostsQueryOptions!, $username: String!) {\n      pinnedPosts { title repl { url } user { username } }\n      siteBanner { id message }\n      trendingReplPosts(count: $count) { repl { id title url description user { username } } }\n      replPosts(options: $options) { items { repl { title url description user { username } } } }\n      userByUsername(username: $username) { presenceStatus { lastSeen isOnline } }\n    }",
    "trending": "query ReplPosts($options: ReplPostsQueryOptions) {replPosts(options: $options) {\n\t\t\titems {\n\t \t\t\tid\n\t\t \t\ttitle\n\t\t\t\tshowHosted\n\t\t \t\tcommentCount\n\t\t\t\tisPinned\n\t\t \t\tisHidden\n\t\t\t\tisLocked\n\t\t \t\ttimeCreated\n\t\t\t\ttimeUpdated\n\t\t \t\tbody\n\t\t\t\turl\n\t\t \t\tuser {\n\t\t\t\t\tusername\n\t\t\t\t}\n\t\t \t\tboard {\n\t\t\t\t\tid\n\t\t\t\t}\n\t\t \t\trepl {\n\t\t\t\t\tid\n\t\t\t\t}\n\t\t \t\treplComment {\n\t\t\t\t\tid\n\t\t \t\t\tuser {\n\t\t\t\t\t\tid\n\t\t\t\t\t}\n\t\t\t\t}\n\t\t\t}\n\t\t}}",
    "homepageTrending": """query HomeTrendingRepls { 
	trendingReplPosts(count: 6) { 
		repl { 
			id ...ReplPostReplCardRepl __typename 
		} 
	} 
}

fragment ReplPostReplCardRepl on Repl {
  id iconUrl description(plainText: true) ...ReplPostReplInfoRepl ...ReplStatsRepl ...ReplLinkRepl tags {
    id ...PostsFeedNavTag __typename 
  } owner {
    ... on Team {
      id username url image __typename 
    } 
    
    ... on User {
      id username url image __typename
    } __typename 
  } __typename 
} 

fragment ReplPostReplInfoRepl on Repl { 
  id title description(plainText: true) imageUrl iconUrl templateInfo { 
    label iconUrl __typename
  } __typename 
} 

fragment ReplStatsRepl on Repl { 
  id likeCount runCount commentCount __typename 
} 

fragment ReplLinkRepl on Repl { 
  id url nextPagePathname __typename 
} 

fragment PostsFeedNavTag on Tag { 
  id isOfficial __typename
}""",
    "follows": "query FollowModalFollows($username: String!, $after: String, $count: Int) {userByUsername(username: $username) {follows(after: $after, count: $count) {\n\t\t\titems {\n\t \t\t\tid\n\t\t\t\tusername\n\t\t\t\tfirstName\n\t\t\t\tlastName\n\t\t\t\tlocale\n\t\t\t\tisVerified\n\t\t\t\tdisplayName\n\t\t\t\tfullName\n\t\t\t\turl\n\t\t\t\tbio\n\t\t\t\tsocials {\n\t\t\t\t\tid\n\t\t\t \t\turl\n\t\t\t\t\ttype\n\t\t\t\t}\n\t\t\t\troles {\n\t\t\t\t\tid\n\t\t\t \t\tkey\n\t\t\t\t\tname\n\t\t\t \t\ttagline\n\t\t\t\t}\n\t\t\t\tisFollowedByCurrentUser\n\t\t\t\tisFollowingCurrentUser\n\t\t\t\tisBlockedByCurrentUser\n\t\t\t\tisBlockingCurrentUser\n\t\t\t\tisLoggedIn\n\t\t\t\tisSubscribed\n\t\t\t\ttimeCreated\n\t\t\t\tfollowerCount\n\t\t\t\tfollowCount\n\t\t\t\tisHacker\n\t\t\t\timage\n\t\t\t\tcoverImage {\n\t\t\t\t\turl\n\t\t\t \t\toffsetY\n\t\t\t\t}\n\t\t\t\tpresenceStatus {\n\t\t\t\t\tlastSeen\n\t\t\t \t\tisOnline\n\t\t\t\t}\n\t\t\t}\n\t \t\tpageInfo {\n\t\t \t\thasNextPage\n\t\t \t\tnextCursor\n\t\t\t}\n\t\t}}}",
    "addMultiplayer": "mutation AddMultiplayerUser($username: String!, $replId: String!, $type: String!) {addMultiplayerUser(username: $username, replId: $replId, type: $type) {id}}",
    "followers": "query FollowModalFollowers($username: String!, $after: String, $count: Int) {userByUsername(username: $username) {followers(after: $after, count: $count) {\n\t\t\titems {\n\t \t\t\tid\n\t\t\t\tusername\n\t\t\t\tfirstName\n\t\t\t\tlastName\n\t\t\t\tlocale\n\t\t\t\tisVerified\n\t\t\t\tdisplayName\n\t\t\t\tfullName\n\t\t\t\turl\n\t\t\t\tbio\n\t\t\t\tsocials {\n\t\t\t\t\tid\n\t\t\t \t\turl\n\t\t\t\t\ttype\n\t\t\t\t}\n\t\t\t\troles {\n\t\t\t\t\tid\n\t\t\t \t\tkey\n\t\t\t\t\tname\n\t\t\t \t\ttagline\n\t\t\t\t}\n\t\t\t\tisFollowedByCurrentUser\n\t\t\t\tisFollowingCurrentUser\n\t\t\t\tisBlockedByCurrentUser\n\t\t\t\tisBlockingCurrentUser\n\t\t\t\tisLoggedIn\n\t\t\t\tisSubscribed\n\t\t\t\ttimeCreated\n\t\t\t\tfollowerCount\n\t\t\t\tfollowCount\n\t\t\t\tisHacker\n\t\t\t\timage\n\t\t\t\tcoverImage {\n\t\t\t\t\turl\n\t\t\t \t\toffsetY\n\t\t\t\t}\n\t\t\t\tpresenceStatus {\n\t\t\t\t\tlastSeen\n\t\t\t \t\tisOnline\n\t\t\t\t}\n\t\t\t}\n\t \t\tpageInfo {\n\t\t \t\thasNextPage\n\t\t \t\tnextCursor\n\t\t\t}\n\t\t}}}",
    "profileRepls": "query ProfilePublicRepls($username: String!, $after: String, $search: String, $count: Int) {user: userByUsername(username: $username) {profileRepls: profileRepls(after: $after, search: $search, count: $count) {\n\t\t\titems {\n\t \t\t\tid\n\t\t\t \tisProject\n\t\t\t \tisPrivate\n\t\t\t \tisStarred\n\t\t\t \ttitle\n\t\t\t \tslug\n\t\t\t \timageUrl\n\t\t\t \tfolderId\n\t\t\t \tisRenamed\n\t\t\t \tcommentCount\n\t\t\t \tlikeCount\n\t\t\t \tcurrentUserDidLike\n\t\t\t \ttemplateCategory\n\t\t\t \twasPosted\n\t\t\t \twasPublished\n\t\t\t \tlayoutState\n\t\t\t \tlanguage\n\t\t\t \towner: user {\n\t\t\t \t\tid\n\t\t\t\t\tusername\n\t\t\t\t\tfirstName\n\t\t\t\t\tlastName\n\t\t\t\t\tlocale\n\t\t\t\t\tisVerified\n\t\t\t\t\tdisplayName\n\t\t\t\t\tfullName\n\t\t\t\t\turl\n\t\t\t\t\tbio\n\t\t\t\t\tsocials {\n\t\t\t\t\t\tid\n\t\t\t\t \t\turl\n\t\t\t\t\t\ttype\n\t\t\t\t\t}\n\t\t\t\t\troles {\n\t\t\t\t\t\tid\n\t\t\t\t \t\tkey\n\t\t\t\t\t\tname\n\t\t\t\t \t\ttagline\n\t\t\t\t\t}\n\t\t\t\t\tisFollowedByCurrentUser\n\t\t\t\t\tisFollowingCurrentUser\n\t\t\t\t\tisBlockedByCurrentUser\n\t\t\t\t\tisBlockingCurrentUser\n\t\t\t\t\tisLoggedIn\n\t\t\t\t\tisSubscribed\n\t\t\t\t\ttimeCreated\n\t\t\t\t\tfollowerCount\n\t\t\t\t\tfollowCount\n\t\t\t\t\tisHacker\n\t\t\t\t\timage\n\t\t\t\t\tcoverImage {\n\t\t\t\t\t\turl\n\t\t\t\t \t\toffsetY\n\t\t\t\t\t}\n\t\t\t\t\tpresenceStatus {\n\t\t\t\t\t\tlastSeen\n\t\t\t\t \t\tisOnline\n\t\t\t\t\t}\n\t\t\t\t}\n\t\t\t\torigin {\n\t\t\t\t\tid\n\t\t\t \t\ttitle\n\t\t\t\t}\n\t\t\t\tlang {\n\t\t\t\t\tid\n\t\t\t \t\tdisplayName\n\t\t\t\t\tcanUseShellRunner\n\t\t\t\t}\n\t\t\t\ticonUrl\n\t\t\t\ttemplateLabel\n\t\t\t\turl\n\t\t\t\tinviteUrl\n\t\t\t\tmultiplayerInvites {\n\t\t\t\t\temail\n\t\t\t \t\treplId\n\t\t\t\t\ttype\n\t\t\t\t}\n\t\t\t\thistoryUrl\n\t\t\t\tanalyticsUrl\n\t\t\t\trootOriginReplUrl\n\t\t\t\ttimeCreated\n\t\t\t\ttimeUpdated\n\t\t\t\tisOwner\n\t\t\t\tconfig {\n\t\t\t\t\tisServer\n\t\t\t \t\tgitRemoteUrl\n\t\t\t\t\tdomain\n\t\t\t \t\tisVnc\n\t\t\t \t\tdoClone\n\t\t\t\t}\n\t\t\t\tpinnedToProfile\n\t\t\t\tsize\n\t\t\t\thostedUrl\n\t\t\t\thostedUrlDotty: hostedUrl(dotty: true)\n\t\t\t\thostedUrlDev: hostedUrl(dev: true)\n\t\t\t\thostedUrlNoCustom: hostedUrl(noCustomDomain: true)\n\t\t\t\tterminalUrl\n\t\t\t\tcurrentUserPermissions {\n\t\t\t\t\tchangeTitle\n\t\t\t \t\tchangeDescription\n\t\t\t\t\tchangeImageUrl\n\t\t\t \t\tchangeIconUrl\n\t\t\t\t\tchangeTemplateLabel\n\t\t\t \t\tchangeLanguage\n\t\t\t\t\tchangeConfig\n\t\t\t \t\tchangePrivacy\n\t\t\t\t\tstar\n\t\t\t \t\tpin\n\t\t\t\t\tmove\n\t\t\t \t\tdelete\n\t\t\t\t\tleaveMultiplayer\n\t\t\t \t\teditMultiplayers\n\t\t\t\t\tviewHistory\t\n\t\t\t \t\tcontainerAttach\n\t\t\t\t\tcontainerWrite\n\t\t\t \t\tchangeAlwaysOn\n\t\t\t\t\tlinkDomain\n\t\t\t \t\twriteTests\n\t\t\t\t\tchangeCommentSettings\n\t\t\t \t\tinviteGuests\n\t\t\t\t\tpublish\n\t\t\t \t\tfork\n\t\t\t\t}\n\t\t\t\tdatabase {\n\t\t\t\t\tid\n\t\t\t \t\tkeysCount\n\t\t\t\t\tsizeMB\n\t\t \t\t\tjwt\n\t\t\t\t}\n\t\t\t\ttemplate {\n\t\t\t\t\tid\n\t\t\t\t}\n\t\t\t\tisProjectFork\n\t\t\t\tisModelSolution\n\t\t\t\tisModelSolutionFork\n\t\t\t\tworkspaceCta\n\t\t\t\tsubmission {\n\t\t\t\t\tid\n\t\t\t \t\ttimeSubmitted\n\t\t\t\t\ttimeLastReviewed\n\t\t\t \t\tisGroupSubmission\n\t\t\t\t\tauthor {\n\t\t\t \t\t\tusername\n\t\t\t\t\t}\n\t\t\t \t\tsubmissionGroup {\n\t\t\t\t\t\tusers {\n\t\t\t\t\t\t\tusername\n\t\t\t\t\t\t}\n\t\t\t\t\t}\n\t\t\t\t}\n\t\t\t\tcommentSettings {\n\t\t\t\t\tid\n\t\t\t \t\tenabled\n\t\t\t\t}\n\t\t\t\tpublicForkCount\n\t\t\t\trunCount\n\t\t\t\tisAlwaysOn\n\t\t\t\tisBoosted\n\t\t\t\ttags {\n\t\t\t\t\tid\n\t\t\t \t\tisOfficial\n\t\t\t\t}\n\t\t\t\tlastPublishedAt\n\t\t\t\tmultiplayers {\n\t\t\t\t\tusername\n\t\t\t\t}\n\t\t\t\tnixedLanguage\n\t\t\t\tpublishedAs\n\t\t\t\tattachments {\n\t\t\t\t\tid\n\t\t\t \t\tfileName\n\t\t\t\t\tmimeType\n\t\t\t \t\ttimeCreated\n\t\t\t\t\ttimeUpdated\n\t\t\t \t\tcontents\n\t\t\t\t}\n\t\t\t\tdescription(plainText: true)\n\t\t\t\tmarkdownDescription: description(plainText: false)\n\t\t\t\thasExplainCode\n\t\t\t\thasGenerateCode\n\t\t\t\ttemplateInfo {\n\t\t\t\t\tlabel\n\t\t\t \t\ticonUrl\n\t\t\t\t}\n\t\t\t\tdomains {\n\t\t\t\t\tdomain\n\t\t\t \t\tstate\n\t\t\t\t}\n\t\t\t\tapexProxy\n\t\t\t\treplViewSettings {\n\t\t\t\t\tid\n\t\t\t \t\tdefaultView\n\t\t\t\t\treplFile\n\t\t\t \t\treplImage\n\t\t\t\t}\n\t\t\t\tpowerUpCosts {\n\t\t\t\t\t...on UnauthorizedError {\n\t\t\t \t\t\tmessage\n\t\t\t\t\t}\n\t\t\t \t\t...on NotFoundError {\n\t\t\t\t\t\tmessage\n\t\t\t\t\t}\n\t\t\t \t\t...on PowerUpCostsType {\n\t\t\t\t\t\tboost {\n\t\t\t\t\t\t\tcycles\n\t\t\t\t \t\t\texplanation\n\t\t\t\t\t\t}\n\t\t\t\t\t\talwaysOn {\n\t\t\t\t\t\t\tcycles\n\t\t\t\t \t\t\texplanation\n\t\t\t\t\t\t}\n\t\t\t\t\t}\n\t\t\t\t}\n\t\t\t\tisTutorial\n\t\t\t},\n\t \t\tpageInfo {\n\t\t\t\thasNextPage\n\t\t\t\tnextCursor\n\t\t\t}\n\t\t}}}",
    "block": "mutation SetBlocking($input: SetBlockingInput!) {setBlocking(input: $input) {... on User {\n\t\t\tisBlockedByCurrentUser\n\t \t}, ... on NotFoundError {message}, ... on UnauthorizedError {message}}}",
    "search": "query Search($options: SearchQueryOptions!) {search(options: $options) {...on UserError {message} ...on UnauthorizedError {message} ...on SearchQueryResults {\n\t\t\treplResults {\n\t \t\t\tresults {\n\t\t \t\t\titems {\n\t\t\t\t\t\tid\n\t\t\t\t\t}\n\t\t\t\t}\n\t\t\t}\n\t \t\ttemplateResults {\n\t\t\t\tresults {\n\t\t\t\t\titems {\n\t\t\t\t\t\tid\n\t\t\t\t\t}\n\t\t\t\t}\n\t\t\t}\n\t \t\tfileResults {\n\t\t\t\tresults {\n\t\t\t\t\titems {\n\t\t \t\t\t\trepl {\n\t\t\t \t\t\t\tid\n\t\t\t\t\t\t}\n\t\t\t\t\t}\n\t\t\t\t}\n\t\t\t}\n\t \t\tuserResults {\n\t\t\t\tresults {\n\t\t\t\t\titems {\n\t\t\t\t\t\tusername\n\t\t\t\t\t}\n\t\t\t\t}\n\t\t\t}\n\t \t\tpostResults {\n\t\t\t\tresults {\n\t\t\t\t\titems {\n\t\t\t\t\t\tid\n\t\t\t\t\t}\n\t\t\t\t}\n\t\t\t}\n\t \t\tdocResults {\n\t\t\t\tresults {\n\t\t\t\t\titems {\n\t\t \t\t\t\tpath\n\t\t\t\t\t}\n\t\t\t\t}\n\t\t\t}\n\t \t\ttagResults {\n\t\t\t\tresults {\n\t\t\t\t\titems {\n\t\t \t\t\t\ttag {\n\t\t\t \t\t\t\tid\n\t\t\t\t\t\t\tisOfficial\n\t\t\t\t\t\t}\n\t\t\t\t\t\ttimeLastUsed\n\t\t\t\t\t\treplsCount: numReplsTotal\n\t\t\t\t\t}\n\t\t\t\t}\n\t\t\t}\n\t\t}}}",
    "dashboardCreateFolder": "mutation ReplsDashboardCreateReplFolder($name: String!, $parentId: String, $teamId: Int) {createReplFolder(name: $name, parentId: $parentId, teamId: $teamId) {id, ...ReplsDashboardFolderItemReplFolder, }}, fragment ReplsDashboardFolderItemReplFolder on ReplFolder {id, name, canEdit, pathnames, image, timeCreated, replsCount, folderType}",
    "replUrl": "query Repl($url: String!) {repl(url: $url) {... on Repl {id, title, slug, description, lang {id}, url, timeCreated, timeUpdated, hostedUrl}}}",
    "forkRepl": "mutation ForkReplCreateRepl($input: CreateReplInput!) {createRepl(input: $input) {... on Repl {id}}}",
    "userComments": "query UserByUsername($username: String!, $count: Int!) {userByUsername(username: $username){comments(count: $count) {items {id, body, voteCount, timeCreated, timeUpdated, user {username}, url, post {id}, parentComment {id}, isAuthor, canEdit, canVote, canComment, hasVoted, canReport, hasReported, isAnswer, canSelectAsAnswer, canUnselectAsAnswer}}}}",
    "sendReplComment": "mutation CreateReplComment($input: CreateReplCommentInput!) {createReplComment(input: $input) {...on UserError {message} ...on ReplComment {\n\t\t\tid\n\t \t\tbody\n\t\t\ttimeCreated\n\t \t\ttimeUpdated\n\t\t\tuser {\n\t \t\t\tusername\n\t\t\t}\n\t\t\tpost {\n\t \t\t\tid\n\t\t\t}\n\t \t\trepl {\n\t\t\t\tid\n\t\t\t}\n\t \t\tcanEdit\n\t\t}}}",
    "dashboardRepls": "query ReplsDashboardReplFolderList($path: String!, $starred: Boolean, $after: String, $count: Int) {currentUser {replFolderByPath(path: $path) {\n\t\t\tid\n\t \t\tuserId\n\t\t\tpathnames\n\t \t\tcanEdit\n\t\t\tcanCreateSubFolders\n\t \t\tparent {id}\n\t\t\tfolders {\n\t\t \t\tid\n\t\t \t\tname\n\t\t \t\tcanEdit\n\t\t \t\tpathnames\n\t\t \t\timage\n\t\t \t\ttimeCreated\n\t\t \t}\n\t\t\trepls(starred: $starred, after: $after, count: $count) {items {\n\t\t\t\tid\n\t\t\t \tisProject\n\t\t\t \tisPrivate\n\t\t\t \tisStarred\n\t\t\t \ttitle\n\t\t\t \tslug\n\t\t\t \timageUrl\n\t\t\t \tfolderId\n\t\t\t \tisRenamed\n\t\t\t \tcommentCount\n\t\t\t \tlikeCount\n\t\t\t \tcurrentUserDidLike\n\t\t\t \ttemplateCategory\n\t\t\t \twasPosted\n\t\t\t \twasPublished\n\t\t\t \tlayoutState\n\t\t\t \tlanguage\n\t\t\t \towner: user {\n\t\t\t \t\tid\n\t\t\t\t\tusername\n\t\t\t\t\tfirstName\n\t\t\t\t\tlastName\n\t\t\t\t\tlocale\n\t\t\t\t\tisVerified\n\t\t\t\t\tdisplayName\n\t\t\t\t\tfullName\n\t\t\t\t\turl\n\t\t\t\t\tbio\n\t\t\t\t\tsocials {\n\t\t\t\t\t\tid\n\t\t\t\t \t\turl\n\t\t\t\t\t\ttype\n\t\t\t\t\t}\n\t\t\t\t\troles {\n\t\t\t\t\t\tid\n\t\t\t\t \t\tkey\n\t\t\t\t\t\tname\n\t\t\t\t \t\ttagline\n\t\t\t\t\t}\n\t\t\t\t\tisFollowedByCurrentUser\n\t\t\t\t\tisFollowingCurrentUser\n\t\t\t\t\tisBlockedByCurrentUser\n\t\t\t\t\tisBlockingCurrentUser\n\t\t\t\t\tisLoggedIn\n\t\t\t\t\tisSubscribed\n\t\t\t\t\ttimeCreated\n\t\t\t\t\tfollowerCount\n\t\t\t\t\tfollowCount\n\t\t\t\t\tisHacker\n\t\t\t\t\timage\n\t\t\t\t\tcoverImage {\n\t\t\t\t\t\turl\n\t\t\t\t \t\toffsetY\n\t\t\t\t\t}\n\t\t\t\t\tpresenceStatus {\n\t\t\t\t\t\tlastSeen\n\t\t\t\t \t\tisOnline\n\t\t\t\t\t}\n\t\t\t\t}\n\t\t\t\torigin {\n\t\t\t\t\tid\n\t\t\t \t\ttitle\n\t\t\t\t}\n\t\t\t\tlang {\n\t\t\t\t\tid\n\t\t\t \t\tdisplayName\n\t\t\t\t\tcanUseShellRunner\n\t\t\t\t}\n\t\t\t\ticonUrl\n\t\t\t\ttemplateLabel\n\t\t\t\turl\n\t\t\t\tinviteUrl\n\t\t\t\tmultiplayerInvites {\n\t\t\t\t\temail\n\t\t\t \t\treplId\n\t\t\t\t\ttype\n\t\t\t\t}\n\t\t\t\thistoryUrl\n\t\t\t\tanalyticsUrl\n\t\t\t\trootOriginReplUrl\n\t\t\t\ttimeCreated\n\t\t\t\ttimeUpdated\n\t\t\t\tisOwner\n\t\t\t\tconfig {\n\t\t\t\t\tisServer\n\t\t\t \t\tgitRemoteUrl\n\t\t\t\t\tdomain\n\t\t\t \t\tisVnc\n\t\t\t \t\tdoClone\n\t\t\t\t}\n\t\t\t\tpinnedToProfile\n\t\t\t\tsize\n\t\t\t\thostedUrl\n\t\t\t\thostedUrlDotty: hostedUrl(dotty: true)\n\t\t\t\thostedUrlDev: hostedUrl(dev: true)\n\t\t\t\thostedUrlNoCustom: hostedUrl(noCustomDomain: true)\n\t\t\t\tterminalUrl\n\t\t\t\tcurrentUserPermissions {\n\t\t\t\t\tchangeTitle\n\t\t\t \t\tchangeDescription\n\t\t\t\t\tchangeImageUrl\n\t\t\t \t\tchangeIconUrl\n\t\t\t\t\tchangeTemplateLabel\n\t\t\t \t\tchangeLanguage\n\t\t\t\t\tchangeConfig\n\t\t\t \t\tchangePrivacy\n\t\t\t\t\tstar\n\t\t\t \t\tpin\n\t\t\t\t\tmove\n\t\t\t \t\tdelete\n\t\t\t\t\tleaveMultiplayer\n\t\t\t \t\teditMultiplayers\n\t\t\t\t\tviewHistory\t\n\t\t\t \t\tcontainerAttach\n\t\t\t\t\tcontainerWrite\n\t\t\t \t\tchangeAlwaysOn\n\t\t\t\t\tlinkDomain\n\t\t\t \t\twriteTests\n\t\t\t\t\tchangeCommentSettings\n\t\t\t \t\tinviteGuests\n\t\t\t\t\tpublish\n\t\t\t \t\tfork\n\t\t\t\t}\n\t\t\t\tdatabase {\n\t\t\t\t\tid\n\t\t\t \t\tkeysCount\n\t\t\t\t\tsizeMB\n\t\t \t\t\tjwt\n\t\t\t\t}\n\t\t\t\ttemplate {\n\t\t\t\t\tid\n\t\t\t\t}\n\t\t\t\tisProjectFork\n\t\t\t\tisModelSolution\n\t\t\t\tisModelSolutionFork\n\t\t\t\tworkspaceCta\n\t\t\t\tsubmission {\n\t\t\t\t\tid\n\t\t\t \t\ttimeSubmitted\n\t\t\t\t\ttimeLastReviewed\n\t\t\t \t\tisGroupSubmission\n\t\t\t\t\tauthor {\n\t\t\t \t\t\tusername\n\t\t\t\t\t}\n\t\t\t \t\tsubmissionGroup {\n\t\t\t\t\t\tusers {\n\t\t\t\t\t\t\tusername\n\t\t\t\t\t\t}\n\t\t\t\t\t}\n\t\t\t\t}\n\t\t\t\tcommentSettings {\n\t\t\t\t\tid\n\t\t\t \t\tenabled\n\t\t\t\t}\n\t\t\t\tpublicForkCount\n\t\t\t\trunCount\n\t\t\t\tisAlwaysOn\n\t\t\t\tisBoosted\n\t\t\t\ttags {\n\t\t\t\t\tid\n\t\t\t \t\tisOfficial\n\t\t\t\t}\n\t\t\t\tlastPublishedAt\n\t\t\t\tmultiplayers {\n\t\t\t\t\tusername\n\t\t\t\t}\n\t\t\t\tnixedLanguage\n\t\t\t\tpublishedAs\n\t\t\t\tattachments {\n\t\t\t\t\tid\n\t\t\t \t\tfileName\n\t\t\t\t\tmimeType\n\t\t\t \t\ttimeCreated\n\t\t\t\t\ttimeUpdated\n\t\t\t \t\tcontents\n\t\t\t\t}\n\t\t\t\tdescription(plainText: true)\n\t\t\t\tmarkdownDescription: description(plainText: false)\n\t\t\t\thasExplainCode\n\t\t\t\thasGenerateCode\n\t\t\t\ttemplateInfo {\n\t\t\t\t\tlabel\n\t\t\t \t\ticonUrl\n\t\t\t\t}\n\t\t\t\tdomains {\n\t\t\t\t\tdomain\n\t\t\t \t\tstate\n\t\t\t\t}\n\t\t\t\tapexProxy\n\t\t\t\treplViewSettings {\n\t\t\t\t\tid\n\t\t\t \t\tdefaultView\n\t\t\t\t\treplFile\n\t\t\t \t\treplImage\n\t\t\t\t}\n\t\t\t\tpowerUpCosts {\n\t\t\t\t\t...on UnauthorizedError {\n\t\t\t \t\t\tmessage\n\t\t\t\t\t}\n\t\t\t \t\t...on NotFoundError {\n\t\t\t\t\t\tmessage\n\t\t\t\t\t}\n\t\t\t \t\t...on PowerUpCostsType {\n\t\t\t\t\t\tboost {\n\t\t\t\t\t\t\tcycles\n\t\t\t\t \t\t\texplanation\n\t\t\t\t\t\t}\n\t\t\t\t\t\talwaysOn {\n\t\t\t\t\t\t\tcycles\n\t\t\t\t \t\t\texplanation\n\t\t\t\t\t\t}\n\t\t\t\t\t}\n\t\t\t\t}\n\t\t\t\tisTutorial\n\t\t\t}\n\t \t\tpageInfo {nextCursor}\n\t\t}}}}",
    "follow": "mutation SetFollowing($input: setFollowingInput!) {setFollowing(input: $input) {... on FollowResult {targetUser {\n\t\t\tisFollowedByCurrentUser, followerCount\n\t \t}}, ... on NotFoundError {message}, ... on UnauthorizedError {message}, ... on UserError {message}}}",
    "restoreRepl": "mutation Mutation($title: String!) {clui {trash {restore(title: $title) {...CluiOutput}}}}, fragment CluiOutput on CluiOutput {... on CluiSuccessOutput {message, json}, ... on CluiErrorOutput {error, json}, ... on CluiMarkdownOutput {markdown}, ... on CluiComponentOutput {component}, ... on CluiTableOutput {columns {label, key}, rows}}",
    "login": "mutation Login($username: String!, $password: String!) {\n  login(username: $username, password: $password) {\n    ... on Auth {\n      token\n      user {\n        email\n        username\n      }\n    }\n\n    ... on UserError {\n      message\n    }\n\n\t\t__typename\n  }\n}",
    "usersWhoLikedRepl": "query Votes($url: String, $after: String) {repl(url: $url) {...on Repl {posts(count: 100) {items {votes(count: 100, after: $after) {items {user {username}} pageInfo {nextCursor}}}}}}}",
    "generateCode": """query GenerateCode($input: GenerateCodeInput!) {currentUser{id}generateCode(input: $input){...on GenerateCodeResult{code}}}""",
    "reportRepl": """mutation ReportRepl($replId: String, $reason: String!) { createBoardReport(replId: $replId, reason: $reason) { id } }""",
    "bounties": """query Bounties($after: String) {
	user: currentUser { username }
  bountySearch(input: { searchQuery: "", count: 10, after: $after }) {
    ...on BountySearchConnection {
      items {
				isUnlisted: isUnlisted
				user { username }

				applications {
					user { username }
					status
				}

				status
        
				deadline
				latestSubmission { review { isAccepted } }

        solverPayout
      }
      pageInfo {
        hasAfter: hasNextPage
        after: nextCursor
      }
    }
    ...on UserError { message }
    ...on UnauthorizedError { message }
  }
}""",
    "setTheme": "mutation SetActiveTheme($input: SetActiveThemeInput!) {setActiveTheme(input: $input) {...on CustomTheme {id}}}",
    "deleteTheme": "mutation DeleteTheme($input: DeleteThemeInput!) {deleteTheme(input: $input) {...on CustomTheme {id}}}",
    "updateTheme": "mutation UpdateTheme($input: UpdateThemeInput!) {updateTheme(input: $input) {...CustomTheme}} fragment CustomTheme on CustomTheme {id title currentUserInstalledThemeVersion {id} hasUnpublishedChanges isInstalledByCurrentUser canCurrentUserInstallUpdate isCurrentUserThemeAuthor latestThemeVersion {...ThemeVersion} draftThemeVersion {...ThemeVersion} author {username} status colorScheme} fragment ThemeVersion on ThemeVersion {id description values {editor {syntaxHighlighting {tags {name modifiers} values}} global {backgroundRoot backgroundDefault backgroundHigher backgroundHighest backgroundOverlay foregroundDefault foregroundDimmer foregroundDimmest outlineDimmest outlineDimmer outlineDefault outlineStronger outlineStrongest accentPrimaryDimmest accentPrimaryDimmer accentPrimaryDefault accentPrimaryStronger accentPrimaryStrongest accentPositiveDimmest accentPositiveDimmer accentPositiveDefault accentPositiveStronger accentPositiveStrongest accentNegativeDimmest accentNegativeDimmer accentNegativeDefault accentNegativeStronger accentNegativeStrongest redDimmest redDimmer redDefault redStronger redStrongest orangeDimmest orangeDimmer orangeDefault orangeStronger orangeStrongest yellowDimmest yellowDimmer yellowDefault yellowStronger yellowStrongest limeDimmest limeDimmer limeDefault limeStronger limeStrongest greenDimmest greenDimmer greenDefault greenStronger greenStrongest tealDimmest tealDimmer tealDefault tealStronger tealStrongest blueDimmest blueDimmer blueDefault blueStronger blueStrongest blurpleDimmest blurpleDimmer blurpleDefault blurpleStronger blurpleStrongest purpleDimmest purpleDimmer purpleDefault purpleStronger purpleStrongest magentaDimmest magentaDimmer magentaDefault magentaStronger magentaStrongest pinkDimmest pinkDimmer pinkDefault pinkStronger pinkStrongest greyDimmest greyDimmer greyDefault greyStronger greyStrongest brownDimmest brownDimmer brownDefault brownStronger brownStrongest black white}}}",
    "installTheme": "mutation UninstallTheme($input: UninstallThemeInput!) {uninstallTheme(input: $input) {...on CustomTheme {id}}}",
    "uninstallTheme": "mutation InstallTheme($input: InstallThemeInput!) {installTheme(input: $input) {...on CustomTheme {id}}}",
    "publishTheme": "mutation PublishTheme($input: PublishThemeInput!) {publishTheme(input: $input) {...on CustomTheme {id}}}",
    "unpublishTheme": "mutation UnpublishTheme($input: UnpublishThemeInput!) {unpublishTheme(input: $input) {...on CustomTheme {id}}}",
    "sonicxTheme": "mutation {setActiveTheme(input: {themeId: 1227}) {...on CustomTheme {id}}}",
    "searchTheme": "query SearchThemes($input: ThemesSearchInput!) {themesSearch(input: $input) {...on CustomThemeConnection {pageInfo {nextCursor} items {...CustomTheme}}}} fragment CustomTheme on CustomTheme {id title currentUserInstalledThemeVersion {id} hasUnpublishedChanges isInstalledByCurrentUser canCurrentUserInstallUpdate isCurrentUserThemeAuthor latestThemeVersion {...ThemeVersion} draftThemeVersion {...ThemeVersion} author {username} status colorScheme} fragment ThemeVersion on ThemeVersion {id description values {editor {syntaxHighlighting {tags {name modifiers} values}} global {backgroundRoot backgroundDefault backgroundHigher backgroundHighest backgroundOverlay foregroundDefault foregroundDimmer foregroundDimmest outlineDimmest outlineDimmer outlineDefault outlineStronger outlineStrongest accentPrimaryDimmest accentPrimaryDimmer accentPrimaryDefault accentPrimaryStronger accentPrimaryStrongest accentPositiveDimmest accentPositiveDimmer accentPositiveDefault accentPositiveStronger accentPositiveStrongest accentNegativeDimmest accentNegativeDimmer accentNegativeDefault accentNegativeStronger accentNegativeStrongest redDimmest redDimmer redDefault redStronger redStrongest orangeDimmest orangeDimmer orangeDefault orangeStronger orangeStrongest yellowDimmest yellowDimmer yellowDefault yellowStronger yellowStrongest limeDimmest limeDimmer limeDefault limeStronger limeStrongest greenDimmest greenDimmer greenDefault greenStronger greenStrongest tealDimmest tealDimmer tealDefault tealStronger tealStrongest blueDimmest blueDimmer blueDefault blueStronger blueStrongest blurpleDimmest blurpleDimmer blurpleDefault blurpleStronger blurpleStrongest purpleDimmest purpleDimmer purpleDefault purpleStronger purpleStrongest magentaDimmest magentaDimmer magentaDefault magentaStronger magentaStrongest pinkDimmest pinkDimmer pinkDefault pinkStronger pinkStrongest greyDimmest greyDimmer greyDefault greyStronger greyStrongest brownDimmest brownDimmer brownDefault brownStronger brownStrongest black white}}}",
    "currentUserTheme": "query {currentUser {authoredThemes(input: {}) {...on CustomThemeConnection {items {...CustomTheme}}} installedThemes(input: {count: 100}) {...on InstalledThemeConnection {items {customTheme {...CustomTheme}}}}}} fragment CustomTheme on CustomTheme {id title currentUserInstalledThemeVersion {id} hasUnpublishedChanges isInstalledByCurrentUser canCurrentUserInstallUpdate isCurrentUserThemeAuthor latestThemeVersion {...ThemeVersion} draftThemeVersion {...ThemeVersion} author {username} status colorScheme} fragment ThemeVersion on ThemeVersion {id description values {editor {syntaxHighlighting {tags {name modifiers} values}} global {backgroundRoot backgroundDefault backgroundHigher backgroundHighest backgroundOverlay foregroundDefault foregroundDimmer foregroundDimmest outlineDimmest outlineDimmer outlineDefault outlineStronger outlineStrongest accentPrimaryDimmest accentPrimaryDimmer accentPrimaryDefault accentPrimaryStronger accentPrimaryStrongest accentPositiveDimmest accentPositiveDimmer accentPositiveDefault accentPositiveStronger accentPositiveStrongest accentNegativeDimmest accentNegativeDimmer accentNegativeDefault accentNegativeStronger accentNegativeStrongest redDimmest redDimmer redDefault redStronger redStrongest orangeDimmest orangeDimmer orangeDefault orangeStronger orangeStrongest yellowDimmest yellowDimmer yellowDefault yellowStronger yellowStrongest limeDimmest limeDimmer limeDefault limeStronger limeStrongest greenDimmest greenDimmer greenDefault greenStronger greenStrongest tealDimmest tealDimmer tealDefault tealStronger tealStrongest blueDimmest blueDimmer blueDefault blueStronger blueStrongest blurpleDimmest blurpleDimmer blurpleDefault blurpleStronger blurpleStrongest purpleDimmest purpleDimmer purpleDefault purpleStronger purpleStrongest magentaDimmest magentaDimmer magentaDefault magentaStronger magentaStrongest pinkDimmest pinkDimmer pinkDefault pinkStronger pinkStrongest greyDimmest greyDimmer greyDefault greyStronger greyStrongest brownDimmest brownDimmer brownDefault brownStronger brownStrongest black white}}}",
    "getTheme": "query {customThemeById(input: {themeId: {}}) {...on CustomTheme {id title}}}",
    "currentUserCycles": "query {currentUser {cycles {balance {...on CyclesBalance {cycles lastUpdated}} transactions {items {id principal_user_id cycles type time_created}}}}}",
    "getBountiesQuery": "query BountiesPageSearch($input: BountySearchInput!) {\n  bountySearch(input: $input) {\n    __typename\n    ... on BountySearchConnection {\n      items {\n        ...BountyCard\n        __typename\n      }\n      pageInfo {\n        hasNextPage\n        nextCursor\n        __typename\n      }\n      __typename\n    }\n    ... on UserError {\n      message\n      __typename\n    }\n    ... on UnauthorizedError {\n      message\n      __typename\n    }\n  }\n}\n\nfragment BountyCard on Bounty {\n  id\n  title\n  descriptionPreview\n  cycles\n  deadline\n  status\n  slug\n  solverPayout\n  timeCreated\n  applicationCount\n  solver {\n    id\n    username\n    image\n    url\n    __typename\n  }\n  user {\n    id\n    username\n    image\n    url\n    __typename\n  }\n  __typename\n}\n",
    "tipQuery": 'query TipRepl($id: String!) {\n  repl(id: $id) {\n    ... on Repl {\n      user {\n        ... on User {\n          id\n          ...TipSurfaceOwnerFragment\n          __typename\n        }\n        __typename\n      }\n      ...TipReplFragment\n      ...TopTipperReplLeaderboard\n      __typename\n    }\n    __typename\n  }\n  currentUser {\n    id\n    ...IsTippingAvailableForSender\n    __typename\n  }\n}\n\nfragment TipSurfaceOwnerFragment on User {\n  id\n  username\n  ...IsTippingAvailableForRecipient\n  __typename\n}\n\nfragment IsTippingAvailableForRecipient on User {\n  id\n  hasPrivacyRole\n  isVerified\n  isGated: gate(feature: "flag-tip-repl")\n  __typename\n}\n\nfragment TipReplFragment on Repl {\n  id\n  slug\n  user {\n    id\n    __typename\n  }\n  totalCyclesTips\n  currentUserTotalTips\n  __typename\n}\n\nfragment TopTipperReplLeaderboard on Repl {\n  id\n  topTippers {\n    ...TopTippersFragment\n    __typename\n  }\n  __typename\n}\n\nfragment TopTippersFragment on TipperUser {\n  user {\n    id\n    username\n    url\n    image\n    __typename\n  }\n  totalCyclesTipped\n  __typename\n}\n\nfragment IsTippingAvailableForSender on CurrentUser {\n  id\n  hasPrivacyRole\n  isVerified\n  __typename\n}\n',
    "reportUser": "mutation ReportUser($reportedUserId: Int, $reason: String!) {\n  createBoardReport(reportedUserId: $reportedUserId, reason: $reason) {\n    __typename\n    id\n    reportedUser {\n      id\n      __typename\n    }\n  }\n}\n",
    "changeBanner": "mutation CoverImageUpdate($input: SetUserCoverImageInput!) {\n  setUserCoverImage(input: $input) {\n    ... on CurrentUser {\n      id\n      ...CoverImageCurrentUser\n      __typename\n    }\n    __typename\n  }\n}\n\nfragment CoverImageCurrentUser on CurrentUser {\n  id\n  coverImage {\n    url\n    offsetY\n    __typename\n  }\n  __typename\n}\n",
    "createChatMessage": "mutation ThreadComment($replId: String!, $anchorId: String!, $annotationMessage: AnnotationMessageInput!, $highlight: AnnotationHighlightInput) {createAnnotationMessage(replId: $replId, anchorId: $anchorId, annotationMessage: $annotationMessage, highlight: $highlight) {...on AnnotationAnchor {id} ...on UserError {message}}}",
    "markMessageAsSeen": "mutation MarkMessagesSeen($replId: String!, $threadId: String) {markMessagesAsSeen(replId: $replId, threadId: $threadId) {...on AnnotationMessageList {messages {id anchor {id}}} ...on UserError {message}}}",
    "getReplAnnotations": "query Repl($url: String, $id: String) {repl(url: $url, id: $id) {...on Repl {id annotationAnchors {id isGeneral messages {id seen anchor {id} user {username bio} content {...on TextMessageContentType {text}}}}}}}",
    "chatInit": """mutation CreateAnnotationAnchor($annotationAnchor: AnnotationAnchorInput!, $annotationMessage: AnnotationMessageInput, $highlight: AnnotationHighlightInput) {
  createAnnotationAnchor(
    annotationAnchor: $annotationAnchor
    annotationMessage: $annotationMessage
    highlight: $highlight
  ) {
    ... on UserError {
      message
      __typename
    }
    ... on AnnotationAnchor {
      id
      path
      isResolved
      isGeneral
      messages {
        id
        user {
          id
          username
        }
        anchor {
          id
        }
        timeCreated
        content {
          ... on TextMessageContentType {
            text
          }
          ... on PreviewMessageContentType {
            preview
          }
          ... on StatusMessageContentType {
            status
          }
          __typename
        }
      }
    }
    __typename
  }
}""",
    "getMultiplayerRepls": """query ReplsDashboardReplFolderList($path: String!, $starred: Boolean, $after: String) {
  currentUser {
    replFolderByPath(path: $path) {
      repls(starred: $starred, after: $after) {
        items {
          id
          ...ReplsDashboardReplItemRepl
        }
        pageInfo {
          nextCursor
        }
      }
    }
  }
}

fragment ReplsDashboardReplItemRepl on Repl {
  id
}""",
    "editComment": "mutation ReplViewCommentsUpdateReplComment($input: UpdateReplCommentInput!) {\n  updateReplComment(input: $input) {\n    ... on ReplComment {\n      id\n      body\n      __typename\n    }\n    ... on UserError {\n      message\n      __typename\n    }\n    __typename\n  }\n}\n",
    "lastEditedRepls": "query HomeRecentRepls($count: Int!) {\n  ownRecentRepls: recentRepls(count: $count, filter: own) {\n    id\n    ...RecentRepl\n    __typename\n  }\n  multiplayerRecentRepls: recentRepls(count: $count, filter: multiplayer) {\n    id\n    ...RecentRepl\n    __typename\n  }\n  currentUser {\n    id\n    username\n    __typename\n  }\n}\n\nfragment RecentRepl on Repl {\n  id\n  title\n  iconUrl\n  ...ReplLinkRepl\n  owner {\n    ... on User {\n      id\n      ...RecentReplUser\n      __typename\n    }\n    ... on Team {\n      id\n      ...RecentReplTeam\n      __typename\n    }\n    __typename\n  }\n  __typename\n}\n\nfragment ReplLinkRepl on Repl {\n  id\n  url\n  nextPagePathname\n  __typename\n}\n\nfragment RecentReplUser on User {\n  id\n  username\n  __typename\n}\n\nfragment RecentReplTeam on Team {\n  id\n  username\n  __typename\n}\n",
}

"""
import { GraphQL } from '@rayhanadev/replit-gql';
import gql from 'graphql-tag';
import * as fs from 'fs';
const client = GraphQL()

let data;

try {
  data = require('./data.json')
} catch {
  try {
    data = require('./dataBackup.json')
  } catch {
    console.error(`Data + DataBackup corrupted or non-existent`)
    process.exit(1)
  }
}

function getBounties(cursor) {
  return new Promise((resolve, reject) => {
    fetch("https://replit.com/graphql?a=" + Math.random(), {
      "cache": "no-cache",
      "headers": {
        'User-Agent': 'Mozilla/5.0',
        'Content-Type': 'application/json',
        'X-Requested-With': 'XMLHttpRequest',
        'Referrer': 'https://replit.com/',
        'Cookie': '',
      },
      "body": JSON.stringify({
        "operationName": "BountiesPageSearch",
        "variables": {
          "input": {
            "after": cursor.toString(),
            "count": 50,
            "searchQuery": "",
            "status": "closed",
            "order": "creationDateDescending"
          }
        },
        "query": "query BountiesPageSearch($input: BountySearchInput!) {\n  bountySearch(input: $input) {\n    __typename\n    ... on BountySearchConnection {\n      items {\n        ...BountyCard\n        __typename\n      }\n      pageInfo {\n        hasNextPage\n        nextCursor\n        __typename\n      }\n      __typename\n    }\n    ... on UserError {\n      message\n      __typename\n    }\n    ... on UnauthorizedError {\n      message\n      __typename\n    }\n  }\n}\n\nfragment BountyCard on Bounty {\n  id\n  title\n  descriptionPreview\n  cycles\n  deadline\n  status\n  slug\n  solverPayout\n  timeCreated\n  applicationCount\n  solver {\n    id\n    username\n    image\n    url\n    __typename\n  }\n  user {\n    id\n    username\n    image\n    url\n    __typename\n  }\n  __typename\n}\n"
      }),
      "method": "POST"
    }).then(async (r) => {
      let j = await r.json()

      if (j.data.bountySearch.__typename !== "BountySearchConnection") {
        reject();
        return;
      }

      if (j.data.bountySearch.pageInfo.hasNextPage) {
        getBounties(cursor + 50).then((re) => {
          resolve([...j.data.bountySearch.items, ...re])
        }).catch(reject)
      } else {
        resolve(j.data.bountySearch.items)
      }
    }).catch(reject)
  })
}

function updateList() {
  getBounties(0).then((bounties) => {
    let tempData = {};

    for (let i = 0; i < bounties.length; i++) {
      if (bounties[i].solver) {
        if (tempData[bounties[i].solver.id]) {
          tempData[bounties[i].solver.id].earned += bounties[i].solverPayout;
          tempData[bounties[i].solver.id].completed++;
        } else {
          tempData[bounties[i].solver.id] = {
            username: bounties[i].solver.username,
            earned: bounties[i].solverPayout,
            completed: 1,
            bountiesMade: 0,
            spent: 0
          }
        }

        if (tempData[bounties[i].user.id]) {
          tempData[bounties[i].user.id].spent += bounties[i].cycles;
          tempData[bounties[i].user.id].bountiesMade++;
        } else {
          tempData[bounties[i].user.id] = {
            username: bounties[i].user.username,
            earned: 0,
            completed: 0,
            bountiesMade: 1,
            spent: bounties[i].cycles
          }
        }
      }
    }

    data = tempData;

    fs.writeFileSync(`./data.json`, JSON.stringify(data))
  }).catch(console.error)
}
updateList()

setInterval(updateList, 3 * 60 * 1000)

export function getData() { return data };

setInterval(() => {
  fs.writeFileSync(`./dataBackup.json`, JSON.stringify(data))
}, 2 * 60 * 1000)
"""

# https://stackoverflow.com/questions/21957131/python-not-finding-file-in-the-same-directory
# import os

# here = os.path.dirname(os.path.abspath(__file__))

# filename = os.path.join(here, "queries.js")

# current = open(filename).read().strip("const queries = ").strip("\nmodule.exports = queries;").split('`,')
# output = {}

# for i in current:
#     _ = i.strip("{").strip("}").strip().replace("`", "")
#     __ = _.split(": ")
#     output[__[0]] = ": ".join(__[1:])

# q.update(output)
